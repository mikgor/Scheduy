function DatetimepickedEvent() {
   var elvalue = document.getElementById("datetimep").value.replace("T", " ");
   document.getElementById("id_deadline").value = elvalue;
}

function Updatedatetimepicker() {
   var elvalue = document.getElementById("id_deadline").value.replace(" ", "T");
   document.getElementById("datetimep").value = elvalue;
}

function ColorpickedEvent() {
   var elvalue = document.getElementById("colorp").value;
   document.getElementById("id_color").value = elvalue;
}

function Updatecolorpicker() {
   var elvalue = document.getElementById("id_color").value;
   document.getElementById("colorp").value = elvalue;
}
