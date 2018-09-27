function DatetimepickedEvent() {
   var deadlineDate = document.getElementById("deadlineDate").value;
   var deadlineTime = document.getElementById("deadlineTime").value;
   if (deadlineDate!='')
      document.getElementById("id_deadline").value = deadlineDate + " " + deadlineTime;
}

function Updatedatetimepicker() {
   var elvalue = document.getElementById("id_deadline").value;
   document.getElementById("deadlineDate").value = elvalue.split(" ")[0];
   document.getElementById("deadlineTime").value = elvalue.split(" ")[1];
   if (elvalue!='')
      displayDeadlineInputs();
}

function ColorpickedEvent() {
   var el = document.getElementById("colorp");
   document.getElementById("id_color").value = el.value;
   el.style.backgroundColor = el.value;
}

function Updatecolorpicker() {
   var elvalue = document.getElementById("id_color").value;
   var el = document.getElementById("colorp");
   el.value = value;
   el.style.backgroundColor = el.value;
}

function AddColorOptions() {
   var el = document.getElementById('colorp');
   var groupColors = [
       'Whitesmoke',
       'Asquamarine',
       'Beige',
       'Burlywood',
       'Coral',
       'Cornflowerblue',
       'Cornsilk',
       'Cadetblue',
       'Crimson',
       'DarkKhaki',
       'DarkOrange',
       'DarkSalmon',
       'DarkSeaGreen',
       'DarkTurquoise',
       'DeepSkyBlue',
       'DodgerBlue',
       'Fuchsia',
       'Gold',
       'GreenYellow',
       'HotPink',
       'IndianRed',
       'Khaki',
       'Lavender'
   ];
   for (var i=0; i<groupColors.length; i++) {
       var option = document.createElement('option');
       option.value = option.text = groupColors[i];
       option.style.backgroundColor = groupColors[i];
       el.add(option);
   }
}

function displayDeadlineInputs() {
   document.getElementById("deadlineInputs").style.display = "block";
   document.getElementById("addDeadlineBtn").style.display = "none";
}

function hideDeadlineInputsAndClear() {
   document.getElementById("deadlineInputs").style.display = "none";
   document.getElementById("addDeadlineBtn").style.display = "inline-block";
   document.getElementById("id_deadline").value = "";
}
