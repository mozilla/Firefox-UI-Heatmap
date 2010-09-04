from django.template import Context, loader
from metrics.dashboard.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse

def index(request):
	title = 'Firefox Tab Heatmap'
			
	t = loader.get_template('tab.html')
	c = Context({
	    'title': title,
	})
	
	return HttpResponse(t.render(c))

def tab(request):
	title = 'Firefox Tab Heatmap'
			
	t = loader.get_template('tab.html')
	c = Context({
	    'title': title,
	})
	
	return HttpResponse(t.render(c))

def heatmap(request):
	title = 'Firefox Heatmap'
	skill = time_on_web = 'all'
	data = 'perc'
	perc_used_by = median_clicks_per_user = False
	all = beginner = intermediate = advanced = False
	show_perc = True;
	
	if 'd' in request.GET:
		data = request.GET['d']			
	
	if 's' in request.GET:
		skill = request.GET['s']		
	
	if 't' in request.GET:
		time_on_web = request.GET['t']	
	
	# Get items	
	items = Heatmap.objects.filter(os = 'Windows', time_on_web = time_on_web, skill = skill).order_by('name')   

	for item in items:
		if data == 'freq':
			item.color = item.heat_freq()
		else:
			item.color = item.heat_perc()	

		item_beginner = Heatmap.objects.filter(os = 'Windows', time_on_web = time_on_web, skill = 'beginner', name = item.name)[0]
		item_intermediate = Heatmap.objects.filter(os = 'Windows', time_on_web = time_on_web, skill = 'intermediate', name = item.name)[0]		
		item_advanced = Heatmap.objects.filter(os = 'Windows', time_on_web = time_on_web, skill = 'advanced', name = item.name)[0]
		
		if data == 'perc':
			beginner = "%0.0f" % (item_beginner.perc * 100) + '%'
			intermediate = "%0.0f" % (item_intermediate.perc * 100) + '%'
			advanced = "%0.0f" % (item_advanced.perc * 100) + '%'
		else:
			beginner = round(item_beginner.clicks_per_user, 2)
			intermediate = round(item_intermediate.clicks_per_user, 2)
			advanced = round(item_advanced.clicks_per_user, 2)
		
		item.perc = "%0.0f" % (item.perc * 100) + '%'
		item.clicks_per_user = round(item.clicks_per_user, 2)		
		item.hover = '<b>' + item.name + '</b>'
		item.hover += '<div style="height: 5px;"></div>' 
		item.hover += 'Used by ' + str(item.perc) + ' of beta users, ' 
		item.hover += 'with an average of ' + str(item.clicks_per_user) + ' clicks per user. '
		item.hover += '<div style="height: 8px;"></div>' 

		item.hover += '<div style="float: left; width: 15%; margin-right: 3%; text-align: right; color: #666; font-size: 11px;">'
		item.hover += '<div style="height: 4px;"></div>'
		item.hover += 'Adv <div style="height: 4px;"></div>'
		item.hover += 'Int <div style="height: 4px;"></div>'
		item.hover += 'Beg <div style="height: 4px;"></div>'				
		item.hover += '</div>'
		
		if data == 'perc':
			item.hover += '<div style="float: left; width: 77%; font-size: 10px; line-height: 1.4em; color: #EFEFEF;">'
			item.hover += '<div style="height: 4px;"></div>'
			item.hover += '<div style="background-color:' + item_advanced.heat_perc() +'; height: 15px; width:' + str(advanced) + '; padding-left: 2px;">' + str(advanced) + '</div>'
			item.hover += '<div style="height: 3px;"></div>'
			item.hover += '<div style="background-color:' + item_intermediate.heat_perc() +'; height: 15px; width:' + str(intermediate) + '; padding-left: 2px;">' + str(intermediate) + '</div>'
			item.hover += '<div style="height: 3px;"></div>'
			item.hover += '<div style="background-color:' + item_beginner.heat_perc() +'; height: 15px; width:' + str(beginner) + '; padding-left: 2px;">' + str(beginner) + '</div>'						
			item.hover += '</div>'
			item.hover += '<div style="height: 0px; clear: both;"></div>'
		else:
			item.hover += '<div style="float: left; width: 77%; font-size: 11px; line-height: 1.4em; ">'		
			item.hover += '<div style="height: 3px;"></div>'
			item.hover += str(advanced)
			item.hover += '<div style="height: 3px;"></div>'
			item.hover += str(intermediate)
			item.hover += '<div style="height: 3px;"></div>'
			item.hover += str(beginner)			
			item.hover += '</div>' 						
			item.hover += '<div style="height: 0px; clear: both;"></div>'
		
		if data == 'freq':
			item.stat = item.clicks_per_user
			show_perc = False
		else:
			item.stat = item.perc
	
	# Get item list
	if data == 'perc':
		items_list = Heatmap.objects.filter(os = 'Windows', skill = skill, time_on_web = time_on_web, is_in_table = True).order_by('-perc')   
	else:
		items_list = Heatmap.objects.filter(os = 'Windows', skill = skill, time_on_web = time_on_web, is_in_table = True).order_by('-clicks_per_user')   
	
	for item in items_list:
		if data == 'freq':
			item.color = item.heat_freq()
		else:
			item.color = item.heat_perc()
		
		if item.category == 'Navigation Toolbar' or item.category == 'Tab Bar' or item.category == 'Vertical Scroll' or item.category == 'Horizontal Scroll':
			item.is_navigation_toolbar = True
		
		if item.category == 'Customization':
			item.is_customization = True
			
		if item.category == 'Bookmarks Menu' or item.category == 'Firefox Menu' or item.category == 'Context Menu':
			item.is_menu = True
			
		item.perc = "%0.0f" % (item.perc * 100) + '%'
		item.clicks_per_user = round(item.clicks_per_user, 2)		
		if data == 'freq':
			item.stat = item.clicks_per_user
		else:
			item.stat = item.perc	

	t = loader.get_template('heatmap.html')
	c = Context({ 'title': title,
	    'items':items,
	    'items_list':items_list,			
			'skill':skill,
			'show_perc':show_perc,
			'data':data,

			'all_skills':skill == 'all',
			'beginner':skill == 'beginner',
			'intermediate':skill == 'intermediate',
			'advanced':skill == 'advanced',

			'all_hours':time_on_web == 'all',
			'low':time_on_web == 'low',
			'medium':time_on_web == 'medium',
			'high':time_on_web == 'high',

			'add_ons':items[12],
			'back':items[0],
			'bookmark_all_tabs':items[1],
			'bookmark_item':items[2],
			'bookmark_star':items[3],
			'bookmarks_bar':items[6],
			'bookmarks_button':items[9],
			'bookmarks_sidebar':items[13],
			'bookmarks_star_edit':items[4],
			'bookmarks_star_remove':items[5],
			'clear_recent_history':items[31],
			'context_menu_customize':items[10],
			'customize_sidebars':items[15],
			'customize':items[11],
			'exit':items[19],
			'feedback_button':items[21],
			'find_in_this_page':items[24],
			'firefox_button':items[25],
			'forward':items[26],
			'help':items[29],
			'history_item':items[32],
			'history_sidebar':items[14],
			'history':items[30],
			'home':items[34],
			'list_all_tabs':items[37],
			'most_visited_drop_down':items[43],
			'new_tab_button':items[46],
			'new_window':items[48],
			'options':items[50],
			'organize_bookmarks':items[51],
			'page_setup':items[53],
			'print_preview':items[54],
			'print':items[52],
			'recent_history_drop_down':items[55],
			'reload_button':items[56],
			'rss':items[59],
			'save_page_as':items[60],
			'scroll_down':items[61],
			'scroll_horizontal_bar':items[35],
			'scroll_left':items[62],
			'scroll_right':items[63],
			'scroll_up':items[64],
			'scroll_vertical_bar':items[86],
			'search_drop_down':items[69],
			'search_enter_key':items[65],
			'search_go_button':items[67],
			'send_link':items[71],
			'show_all_history':items[33],
			'show_in_sidebar':items[72],
			'site_id_ev':items[73],
			'site_id_normal':items[74],
			'site_id_ssl':items[75],
			'stop':items[80],
			'tab_scroll_left':items[81],
			'tab_scroll_right':items[82],
			'tabs_on_top':items[16],
			'toolbar_layout':items[17],
			'url_enter_key':items[27],
			'url_go_button':items[28],
			'url_search_enter_key':items[66],
			'url_search_go_button':items[68],
			'view_bookmarks_toolbar':items[87],		
	})
	
	return HttpResponse(t.render(c))
