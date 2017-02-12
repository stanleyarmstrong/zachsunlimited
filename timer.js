var minutes = 60;
var months = 12;
var hours = 24;
var days = 30;
var seconds = 60;
var dead = 10;
var deathBed = 9;
var bleeding = 8;
var cut = 7;
var aboutToBeStabbed  = 6;
var guyConfrontingYou = 5;
var walkingAlong = 4;
var leftTheHouse = 3;
var gettingReady = 2;
var justWokeUp = 1;
var years;
var data = 10;
switch(data){
  case(dead):
    years = 1;
    break;
  case(deathBed):
    years  = 5;
    break;
  case(bleeding):
    years = 10;
    break;
  case(cut):
    years = 50;
    break;
  case(aboutToBeStabbed):
    years = 100;
    break;
  case(guyConfrontingYou):
    years  = 500;
    break;
  case(walkingAlong):
      years = 1000
      break;
  case(leftTheHouse):
      years = 5000;
      break;
  case(gettingReady):
      years = 10000;
      break;
  case(justWokeUp):
      years = 50000;
      break;
  default:
      years = 666;
      break;
}
function timer(){
  document.getElementById('timer').innerHTML =   years + ":" + months + ":" + days + ":" + hours + ":" + minutes + ":" + seconds;
  seconds--;
  console.log("")
  console.log("A second has passed.");
  if(seconds === 0 ){
    minutes--;
    console.log("A minute has passed.");
    seconds = 60;

  }
  if(minutes === 0){
    hours--;
    console.log("An hour has passed.");
    minutes = 60;
  }
  if(hours === 0){
    days--;
    console.log("A day has passed.")
    hours = 24;
  }
  if(days === 0){
    months--;
    console.log("A month has passed.");
    days = 30;
  }
  if(months === 0){
    years--;
    console.log("A year has passed.")
    months = 12;
  }

};
