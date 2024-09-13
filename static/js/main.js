const FEEDBACK_TEXT = {
    'en': {'pos': 'This information was useful!', 'neg': 'Bad information - did not like it!'},
    'de': {'pos': 'Diese Informationen waren nützlich!', 'neg': 'Schlechte Informationen - hat mir nicht gefallen!'},
}

function getLang() {
    return document.getElementsByTagName('html')[0].getAttribute('lang');
}

function giveFeedback(kind) {
    let http = new XMLHttpRequest();
    http.open('GET', window.location.href + '?feedback=' + kind, true);
    http.send();
    localStorage.setItem(feedbackStorePrefix + window.location.pathname, '1');
}

function hideFeedbackButtons() {
    document.getElementById('fb-pos').setAttribute("hidden", "hidden");
    document.getElementById('fb-neg').setAttribute("hidden", "hidden");
}

const feedbackStorePrefix = 'feedback-';

function feedbackGiven() {
    return localStorage.getItem(feedbackStorePrefix + window.location.pathname) === '1';
}

function addFeedbackButton(id, text, title, kind) {
    if (feedbackGiven()) {
        return;
    }

    let feedbackButton = document.createElement('div');
    feedbackButton.id = id;
    feedbackButton.innerText = text;
    feedbackButton.title = title
    document.body.appendChild(feedbackButton);

    feedbackButton.addEventListener('click', function(e) {
        hideFeedbackButtons();
        giveFeedback(kind);
    })
}

function addFeedbackButtonPositive() {
    addFeedbackButton('fb-pos', '👍', FEEDBACK_TEXT[getLang()]['pos'], 'positive');
}

function addFeedbackButtonNegative() {
    addFeedbackButton('fb-neg', '👎', FEEDBACK_TEXT[getLang()]['neg'], 'negative');
}

window.addEventListener('DOMContentLoaded', function () {
    addFeedbackButtonPositive()
    addFeedbackButtonNegative()
})
