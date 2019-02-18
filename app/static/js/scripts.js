//  Update Values When Checkbox is clicked / unclicked
function updateValues(data, id){
  $("#current_streak" + id).text(data.current_streak);
  $("#longest_streak" + id).text(data.longest_streak);
  $("#weekly_count" + id).text(data.weekly_count);
}


function resetCurrentStreak(habit_id){
  $.post('/_reset_current_streak',{
    id: habit_id
  })
}

// Run upon page load, checks if habit has been completed today and determines
// The current week count
function todayStatus(json){
  var start_day = new Date()
  var yesterday = moment().subtract(1, 'days').startOf('day')
  while ( start_day.getDay() !== 1 ) start_day.setDate(start_day.getDate() -1);
  var start_day = moment(start_day).startOf('day')
  var habit_list = json.habit_list;

  for (var i = 0; i < habit_list.length; i++) {
    var habit_id = habit_list[i]
     if (json.hasOwnProperty(habit_id)){
      var week_count = 0
      json[habit_id].forEach(function(element) {
        if (moment(element) >= start_day){
          week_count ++;
        };
        if (moment(element).isSame(moment(), 'day')){
          $("#checkbox" + habit_id).prop("checked", true)
        }
        if (moment(element) < start_day.subtract(7, 'days')){
          resetCurrentStreak(habit_id)
        }
      });
      if (week_count > 0){
        $("#weekly_count" + habit_id).text(week_count);
      }
      else{
        $("#weekly_count" + habit_id).text(0);
      }

     }
     else{
      $("#weekly_count" + habit_id).text(0);
      if (+$("#current_streak" + habit_id).text() > 0){
      resetCurrentStreak(habit_id);
     }
   }
  }
}




$('.habitCheckbox').click(function() {
  var id = $(this).attr('name')
  var weekly_count = +$("#weekly_count" + id).text();

     if(this.checked){
          $.post('/_complete', {
            id: id,
            weekly_count: weekly_count
          }).done(function(data) {
            updateValues(data, id);
          })
        }
      else {
          $.post('/_undo', {
            id: $(this).attr('name'),
            weekly_count: weekly_count
          }).done(function(data) {
            updateValues(data, id);
          })
        }
    });


 $(function() {

  $.ajax({
    url: '/_check_status',
  }).done(function(json){
    todayStatus(json)

  });
});



