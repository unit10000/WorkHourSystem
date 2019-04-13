
//  做个全屏的构造函数
var FullScreen = function(elem){
  this.elem = document.querySelector(elem);
  this.status  = false;
}
//  全屏
FullScreen.prototype.in = function() {
    this.status = true;
    if (this.elem.requestFullscreen) {
      this.elem.requestFullscreen();
    } else if (this.elem.webkitRequestFullscreen) {
      this.elem.webkitRequestFullscreen();
    } else if (this.elem.mozRequestFullScreen) {
      this.elem.mozRequestFullScreen();
    } else if (this.elem.msRequestFullscreen) {
      //  IE的实现没有实测过，不过据网上的资料说IE11以下可实现的
      this.elem.msRequestFullscreen();
    }else{
        alert('该浏览器不支持全屏显示，请使用谷歌等主流浏览器')
    }

}
//  退出全屏
FullScreen.prototype.out = function() {
    this.status = false;
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
}