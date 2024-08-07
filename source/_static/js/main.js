function pullThankYouCount() {
    // todo: pull thank you count from server
    return Math.floor(Math.random() * 5);
}

function registerThankYou() {
    // todo: post to server to track likes
}

function hideThankYouButton() {
    document.getElementById('ty').setAttribute("hidden", "hidden");
}

function addThankYouButton() {
    let thankYouButton = document.createElement('div');
    thankYouButton.id = 'ty';
    thankYouButton.innerText = '👍';
    thankYouButton.title = 'This information was useful!'

    thankYouButton.addEventListener('click', function(e) {
        hideThankYouButton();
    })
}

function addThankYouCounter() {
    let thankYouCounter = document.createElement('div');
    thankYouCounter.id = 'tyCnt';
    thankYouCounter.innerText = pullThankYouCount() + ' found this useful'
}