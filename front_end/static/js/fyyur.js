
/*
    A JavaScript file that primarily manages venue deletion
*/

$(document).ready(function() {
    
    //A variable that refers to the "x" button and the "Venues" link in the "Successful Deletion" Modal
    //The modal can be found in "templates/pages/show_venue.html"
    var venueRedirectButtons = document.getElementsByClassName("venueRedirect");

    //Function that deletes a specific venue using the AJAX Fetch API
    var deleteVenue = function(e){

        const venue_id = e.target.dataset['id'];
        
        fetch('/venues/' + venue_id, {
            method: "DELETE"
        })

        .then(function() {
            window.location.href = '/venues'
        })

        .catch(function(e) {
            console.log('error', e)
        })

    }

    /*
    Loop that enables a venue to be deleted by clicking on:

    - The "x" at the top-right of the "Successful Deletion" modal
    - The "Venues" link in the same modal
    */

    for(let i = 0; i < venueRedirectButtons.length; i++){
        $(venueRedirectButtons[i]).click(deleteVenue);
    }
    
    
    /*

    Experimental code to modify list of results as the user types in letters and words:
    

    var searchResults = $('ul.items li');
    
    var filterSearchResults = function() {
        var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
        console.log(val);
        
        var filteredResults = function() {
            var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
            return !~text.indexOf(val);
        }

        searchResults.show().filter(filteredResults).hide();
    }

    $("input[name='search_term']").keyup(filterSearchResults);
    
    */



   //Datetime Picker Code
   current_year = new Date().getFullYear();
    
   $('#start_time').datetimepicker({
        format:'Y-m-d h:i A',
        formatTime: 'g:i A',
        step: 30
        
        /*

        Experimental code to restrict shows from being booked for past dates and times

        minDate: new Date()
        yearStart: current_year,
        yearEnd: current_year + 30
        
        */

        
   });

   
//Prevents users from typing in the Start Time field on the "Post a Show" page
$('#start_time').keydown(function(e) {
    e.preventDefault();
    return false;
 });
 
 


});

