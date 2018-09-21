function DatetimepickedEvent() {
   var elvalue = document.getElementById("datetimep").value.replace("T", " ");
   document.getElementById("id_deadline").value = elvalue;
}

function Updatedatetimepicker() {
   var elvalue = document.getElementById("id_deadline").value.replace(" ", "T");
   document.getElementById("datetimep").value = elvalue;
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
