$(document).ready(function(){
    //Скрыть PopUp при загрузке страницы
    PopUpHide();
});
//Функция отображения PopUp
function PopUpShow(){
    $("#deactivate").show();
    $("#senddesc").hide();
    $("#activate").hide();
}
//Функция скрытия PopUp
function PopUpHide(){
    $("#deactivate").hide();
    $("#senddesc").show();
    $("#activate").show();
}