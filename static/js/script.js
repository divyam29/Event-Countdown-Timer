const countDownClock = (number = 100, format = 'seconds') => {

    const d = document;
    const daysElement = d.querySelector('.days');
    const hoursElement = d.querySelector('.hours');
    const minutesElement = d.querySelector('.minutes');
    const secondsElement = d.querySelector('.seconds');
    let countdown;
    convertFormat(format);


    function convertFormat(format) {
        switch (format) {
            case 'seconds':
                return timer(number);
            case 'minutes':
                return timer(number * 60);
            case 'hours':
                return timer(number * 60 * 60);
            case 'days':
                return timer(number * 60 * 60 * 24);
        }
    }

    function timer(seconds) {
        const now = Date.now();
        const then = now + seconds * 1000;

        countdown = setInterval(() => {
            const secondsLeft = Math.round((then - Date.now()) / 1000);

            if (secondsLeft <= 0) {
                clearInterval(countdown);
                return;
            };

            displayTimeLeft(secondsLeft);

        }, 1000);
    }

    function displayTimeLeft(seconds) {
        daysElement.textContent = Math.floor(seconds / 86400);
        hoursElement.textContent = Math.floor((seconds % 86400) / 3600);
        minutesElement.textContent = Math.floor((seconds % 86400) % 3600 / 60);
        secondsElement.textContent = seconds % 60 < 10 ? `0${seconds % 60}` : seconds % 60;
    }
}

var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();

today = mm + '/' + dd + '/' + yyyy;

const date1 = new Date('9/3/2022');
const date2 = new Date(today);
// console.log(date1);
// console.log(date2);
// console.log(getDifferenceInDays(date1, date2));

function getDifferenceInDays(date2, date1) {
    const diffInMs = Math.abs(date2 - date1);
    return diffInMs / (1000 * 60 * 60 * 24);
}
/*
  start countdown
  enter number and format
  days, hours, minutes or seconds
*/
countDownClock(getDifferenceInDays(date1, date2), 'days');