const colors = ["#f6f3e8", "#656565", "#ffffff", "#f6f3e8", "#f6f3e8", "#343434", "#857b6f", "#384048", "#a0a8b0", "#f6f3e8", "#857b6f", "#e5786d", "#ddaa6f", "#ddaa6f", "#e5786d", "#99968b", "#e5786d", "#cae682", "#8ac6f2", "#95e454", "#92a65e", "#cae682", "#ccaa8f", "#8ac6f2", "#e5786d", "#f6f3e8", "#e7f6da", "#95e454", "#95e454", "#cae682", "#cae682", "#ccaa8f", "#ccaa8f", "#99968b", "#99968b", "#cae682", "#cae682", "#99968b", "#95e454", "#95e454", "#cae682", "#cae682", "#ccaa8f", "#ccaa8f", "#99968b", "#8ac6f2", "#95e454", "#cae682", "#8ac6f2", "#cae682", "#8ac6f2", "#95e454", "#95e454", "#cae682", "#cae682", "#99968b", "#e5786d", "#e5786d", "#95e454", "#2cae682", "#8ac6f2", "#ccaa8f", "#f6f3e8"];
const types = [
    {% for css_var in css_variables %}
    "{{ css_var }}",
    {% endfor %}
    'unknown' // special case: a <span> with no class or an un-recognised class
];

let timer;

function toggle() {
    const the_button = document.getElementById("the-button");
    if (timer === undefined) {
        timer = setInterval(change, 500);
        the_button.textContent = "Cease";
        change(); // do it right now, rather than waiting 500ms for the first one
    } else {
        clearTimeout(timer);
        timer = undefined;
        the_button.textContent = "Resume"
    }
}


function change() {
    colors_this_iteration = colors.slice();
    types.forEach(type => {
        // if we've run out of colours, start again
        if (colors_this_iteration.length < 1) {
            colors_this_iteration = colors.slice();
        }
        // randomly pick a colour, use it, and remove it from the array
        index = Math.floor(Math.random() * colors_this_iteration.length);
        let next_color = colors_this_iteration.splice(index, 1)[0];
        document.documentElement.style.setProperty('--' + type, next_color);
    })
}


function transitionOff() {
    // span { transition: unset; }
}
function transitionOn() {
    // span { transition: all 0.5s; }
}
