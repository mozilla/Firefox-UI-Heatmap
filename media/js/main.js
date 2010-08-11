function showDiv(show_id){
  var toShow = document.getElementById(show_id);
  toShow.style.display = "block";
}

function hideDiv(hide_id){
  var toHide = document.getElementById(hide_id);
  toHide.style.display = "none";
}

function showHide(checkbox_id, div1_id, div2_id) {    
	$(checkbox_id).change(function () {
    if ($(this).attr("checked")) {
     	$('#content').fadeTo('fast', 0.1);   		
     	$('#fx_chrome').fadeTo('fast', 0.05);
     	$('#menus_wrapper').show("slow");
      return;
    }
   	$('#menus_wrapper').hide("slow");
   	$('#fx_chrome').fadeTo('medium', 0.2);
   	$('#content').fadeTo('medium', 1);		
	});   
}

function hideHeatmap(checkbox_id) {    
	$(checkbox_id).change(function () {
    if ($(this).attr("checked")) {
     	$('.overlay').hide('fast');   	
     	$('#fx_chrome').fadeTo('fast', 1);    	
      return;
    }
   	$('#fx_chrome').fadeTo('fast', 0.2);
   	$('.overlay').fadeTo('medium', 0.75);		
	});   
}