// js导入语句：（在head里，且js与html文件在同一文件夹里）
//   <script src="lunbo.js"></script>
window.onload = function() {
  document.getElementsByTagName("body")[0].style.height = "535px";
  document.getElementsByTagName("body")[0].style.width = "753px";
  var width = 600;
  var imgs = document.getElementsByTagName("img");
  var box = document.getElementsByTagName("div");
  var num = box[0].children.length; // get img number
  var nowimg = 0;
  for (var i = 0; i < num; i++) {
    imgs[i].style.width = "753px";
    imgs[i].style.height = "535px";
    imgs[i].style.float = "left";
  }
  //box[x],x为图片div的位置，从第一个div开始数第x个就x-1;
  box[0].style.position = "absolute";
  box[0].style.height = "535px";
  box[0].style.left = "0px";
  box[0].style.overflow = "hidden";
  function animate(offset) {
    changeClass(imgs,nowimg+1);
    var left = box[0].style.left ? parseInt(box[0].style.left) : 0;
    var newLeft = left - offset * 753;
    box[0].style.left = newLeft + "px";
    if (newLeft <= -num * 753) {
      box[0].style.left = "0px";
    }
    if (newLeft > 0) {
      box[0].style.left = -(num - 1) * 753 + "px";
    }
  }

  function changeClass(obj, num1) {
    //用于增加和删除类名
    for (var i = 0; i < imgs.length; i += 1) {
      //console.log(circles[i].className);
      if (i != num1) {
        if (obj[i].classList.contains("dong")) {
          obj[i].classList.remove("dong");
        }
        //contains函数：判断是否含有某个类
        //remove函数：删除类
      }
      if (i == num1) {
        obj[i].classList.add("dong");
      }
      //add：增加类名，如果有则不添加
    }
  }
  setInterval(function() {
    animate(1);
    console.log(2);
    if (nowimg < num - 1) {
      nowimg++;
    } else {
      nowimg = 0;
    }
    // 3000为轮播切换速度，3000=3秒
  }, 7000);

  //方法2
  //封装设置元素的无兼容性不透明度
  function setOpacity(obj, num) {
    //获取用户运行浏览器的标识符//标识符里包含浏览器的类型和版本
    var navStr = window.navigator.userAgent;
    //如果是IE
  }
  //图片不透明度过渡动画
  function changeOpacity(obj, sta, end, tim) {
    //obj元素，sta透明度初始值，end透明度结束值，tim透明度变化时间）
    var iOpacity = 0;
    clearInterval(timer2);
    var timer2 = setInterval(function() {
      var speed = Math.ceil(end - sta) / 20; //设置不透明度步进值
      iOpacity += speed;
      if (iOpacity >= end) {
        iOpacity = end;
        clearInterval(timer2);
      }
      setOpacity(obj, iOpacity);
    }, tim);
  }

  //方法1 //想想是否可以用三目运算符直接一句话
  // function getStyle(obj, attr){
  //   //IE
  //   if(obj.currentStyle){
  //     return obj.currentStyle[attr];
  //   }else{
  //     return getComputedStyle(obj, false)[attr];
  //   }
  // }
  // //obj:要实现动画的对象；attr：要实现动画的属性；target：属性动画的最终值
  // function animate(obj, attr, target){
  //   //防止连续移入元素会生成多个计时器，所以进入之前先清除
  //   clearInterval(timer);
  //   obj.timer = setInterval(function(){
  //     //属性当前值
  //     var icur = 0;
  //     if (attr == 'opacity'){
  //       //这里用Math.round()处理是防止出现数据在目标值附近抖动的情况，因为计算机对浮点数的计算存在误差
  //       icur = Math.round(parseFloat(getStyle(obj, attr))*100);
  //     }else{
  //       icur = parseInt(getStyle(obj, attr));
  //     }
  //     //动画速度
  //     var speed = (target - icur) / 8;
  //     speed = speed > 0 ? Math.ceil(speed):
  //     Math.floor(speed);
  //     //检测停止
  //     if(icur == target){
  //       clearInterval(obj.timer);
  //     }else{
  //       if(attr == 'opacity'){
  //         //IE
  //         obj.style.filter = 'alpha(opacity:'+(icur + speed) + ')';
  //         //非IE
  //         obj.style.opacity = (icur+speed)/100;
  //       }else{
  //         obj.style[attr] = icur + speed + 'px';
  //       }
  //     }
  //   },30);
  // }
};
