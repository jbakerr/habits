function updateValues(data, id){
  $("#current_streak" + id).text(data.current_streak);
  $("#longest_streak" + id).text(data.longest_streak);
  $("#weekly_count" + id).text(data.weekly_count);
}


function todayStatus(json){

  var start_day = new Date()
  var yesterday = moment().subtract(1, 'days').startOf('day')
  while ( start_day.getDay() !== 1 ) start_day.setDate(start_day.getDate() -1);
  var start_day = moment(start_day).startOf('day')
  var habit_list = json.habit_list;

  for (var i = 0; i < habit_list.length; i++) {
    var habit = habit_list[i]
     if (json.hasOwnProperty(habit)){
      var week_count = 0
      json[habit].forEach(function(element) {
        if (moment(element) >= start_day){
          week_count ++;
        };
        if (moment(element).isSame(moment(), 'day')){
          $("#checkbox" + habit).prop("checked", true)
        }

      });
      if (week_count > 0){
        $("#weekly_count" + habit).text(week_count);
      }
      else{
        $("#weekly_count" + habit).text(0);
      }

     }
     else{
      $("#weekly_count" + habit).text(0);
     }
  }


}
// Check each habit a user has for completion today
  //  If completed today, check box is checked, else unchecked
// Check the history of each habit to determine current week streak




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
      // TODO: Make sure date is correct and set for midnight
      //  TODO: Make sure page loads with current weekly count

        $.ajax({
          url: '/_check_status',
        }).done(function(json){
          todayStatus(json)

        });
    });



