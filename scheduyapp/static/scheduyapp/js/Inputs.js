function DatetimepickedEvent(e) {
   var date = document.getElementById(e+"Date").value;
   var time = document.getElementById(e+"Time").value;
   if (date!='')
      document.getElementById("id_"+e).value = date + " " + time;
}

function Updatedatetimepicker(e) {
   var elvalue = document.getElementById("id_"+e).value;
   document.getElementById(e+"Date").value = elvalue.split(" ")[0];
   document.getElementById(e+"Time").value = elvalue.split(" ")[1];
   if (elvalue!='')
      displayTimeInputs(e);
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

function displayTimeInputs(e) {
   document.getElementById(e+"Inputs").style.display = "block";
   document.getElementById("add"+e+"Btn").style.display = "none";
}

function hideTimeInputsAndClear(e) {
   document.getElementById(e+"Inputs").style.display = "none";
   document.getElementById("add"+e+"Btn").style.display = "inline-block";
   document.getElementById("id_"+e).value = "";
}

function replaceDate(offset, input) {
   $date = new Date();
   $date.setDate($date.getDate()+offset);
   $month = 0;
   $day = 0;
   if (($date.getMonth()+1) < 10)
      $month = '0' + ($date.getMonth() + 1);
   else
      $month = $date.getMonth() + 1;
   if ($date.getDate() < 10)
      $day = '0' + $date.getDate();
   else
      $day = $date.getDate();
   document.getElementById(input).value = $date.getFullYear() + '-' + $month + '-' + $day;
}
