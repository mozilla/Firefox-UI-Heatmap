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
	skill = 'All'
	perc_used_by = median_clicks_per_user = False
	all = beginner = intermediate = advanced = False
	show_perc = True;
	
	if 'd' in request.GET:
		data = request.GET['d']	
	else:
		data = 'perc'		
		
	items = Heatmap.objects.filter(os = 'Windows', skill = skill).order_by('id')   
	
	if data == 'perc':
		items_list = Heatmap.objects.filter(os = 'Windows', skill = skill, is_in_table = True).order_by('-perc')   
	else:
		items_list = Heatmap.objects.filter(os = 'Windows', skill = skill, is_in_table = True).order_by('-clicks_per_user')   
	
	#items_beginner = Heatmap.objects.filter(os = 1, skill = 1)  
	#items_intermediate = Heatmap.objects.filter(os = 1, skill = 1)
	#items_advanced = Heatmap.objects.filter(os = 1, skill = 1)  
		
	for item in items:
		if data == 'freq':
			item.color = item.heat_freq()
		else:
			item.color = item.heat_perc()	

		item.perc = "%0.0f" % (item.perc * 100) + '%'
		item.clicks_per_user = round(item.clicks_per_user, 2)		
		item.hover = item.name + ': used by ' + str(item.perc) + ' of beta users, with an average of ' + str(item.clicks_per_user) + ' clicks per user'
		if data == 'freq':
			item.stat = item.clicks_per_user
			show_perc = False
		else:
			item.stat = item.perc
		
		#idx = item.id - 1
		#item.beginner_perc = items_beginner[idx].perc
		#item.intermediate_perc = items_intermediate[idx].perc		
		#item.advanced_perc = items_advanced[idx].perc
	
	for item in items_list:
		if data == 'freq':
			item.color = item.heat_freq()
		else:
			item.color = item.heat_perc()
		
		if item.category == 'Navigation Toolbar' or item.category == 'Tab Bar':
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

			'all':all,
			'beginner':beginner,
			'intermediate':intermediate,
			'advanced':advanced,

			'firefox_button':items[4],
			'tab_scroll_left':items[40],
			'tab_scroll_right':items[41],	
			'new_tab_button':items[42],
			'list_all_tabs':items[43],	  
			
			'back':items[26],
			'forward':items[27],
			'recent_history_drop_down':items[28],
			'reload_stop_button':items[28],
			'reload_button':items[29],
			'stop':items[30],
			'home':items[31],
			
			'site_id_normal':items[51],
			'site_id_ev':items[55],
			'site_id_ssl':items[56],		
			
			'url_enter_key':items[54],
			'url_search_enter_key':items[56],	
			
			'url_go_button':items[55],	
			'url_search_go_button':items[59],		
			'most_visited_drop_down':items[58],
			
			'rss':items[32],
			'bookmark_star':items[33],
			'bookmarks_star_edit':items[34],
			'bookmarks_star_remove':items[35],	
			
			'search_drop_down':items[45],
			'search_drop_down_select':items[49],	
			'search_enter_key':items[47],
			'search_go_button':items[48],
			
			'bookmarks_button':items[64],
			'feedback_button':items[60],
			
			'scroll_up':items[36],
			'scroll_down':items[37],
			'scroll_vertical_bar':items[38],	
			
			'scroll_left':items[39],
			'scroll_right':items[40],
			'scroll_horizontal_bar':items[41],
			
			'customize_tabs_on_top':items[0],
			'menu_bar':items[1],
			'bookmarks_bar':items[2],
			'status_bar':items[3],
			
			'new_window':items[5],
			'save_page_as':items[6],
			'send_link':items[7],
			'print':items[8],
			'find_in_this_page':items[11],												
			'history':items[12],
			'customize':items[16],
			'options':items[23],
			'help':items[24],
			'exit':items[25],	
			
			'page_setup':items[9],
			'print_preview':items[11],
			'clear_recent_history':items[13],
			'show_all_history':items[14],
			'history_item':items[15],												
			'tabs_on_top':items[17],			
			'toolbar_layout':items[18],
			'customize_sidebars':items[19],												
			'add_ons':items[22],		
			
			'bookmarks_sidebar':items[20],												
			'history_sidebar':items[21],							
			
			'bookmark_all_tabs':items[65],
			'organize_bookmarks':items[66],
			'view_bookmarks_toolbar':items[67],
			'show_in_sidebar':items[68],
			'bookmark_item':items[69],				
	})
	
	return HttpResponse(t.render(c))
