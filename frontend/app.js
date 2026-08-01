import {get_sessions, delete_session, render_history} from './helper.js'

const ul = document.getElementById("history-list")
const start_button = document.getElementById("start-btn")
const subject = document.getElementById("subject");
const notes = document.getElementById("notes");
const current_session = document.getElementById("current-session")
const active_session_div = document.getElementById("active-session")
const no_active_session_div = document.getElementById("no-active-session")
const error_div = document.getElementById("error-message") // add this in HTML
const start_session_section = document.getElementById("start-session-section")
const url = "http://127.0.0.1:8000"

get_sessions()
function time_intravel(start_time){
    current_time = Date.getTime()

}
async function start_session(event){
    event.preventDefault();
    const response = await fetch(`${url}/api/start`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "subject": subject.value,
            "notes": notes.value
        })
    });
    if (response.ok){
        console.log("Session started")
    }
 
}

async function stop_session(id){
    const response = await fetch(`${url}/api/stop/${id}`,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        }
    });
    if (response.ok){
        const data = await response.json()
        console.log(data)
        start_button.disabled=false
    }
}

async function get_active_session(){
    const response = await fetch(`${url}/api/active-session`)
    if (response.ok){
        const session_data = await response.json()
        if(!session_data || Object.keys(session_data).length === 0){
            start_session_section.style.display="block"
            start_button.disabled = false
            render_current_session(null)
        }
        else{
            start_button.disabled = true
            start_session_section.style.display="none"
            render_current_session(session_data)
            console.log(session_data)
        } 
    }
    else{
        start_button.disabled=false
        start_session_section.style.display="block"
    }
}
function show_timer(start_timer){
    const timer = document.getElementById("timer");

    const current_time = new Date().getTime()
    const start_time = new Date(start_timer)
    const difference = current_time - start_time
    const hours = Math.floor((difference % (1000*60*60*24)) / (1000*60*60))
    const minutes = Math.floor((difference % (1000*60*60)) / (1000*60))
    const seconds = Math.floor((difference % (1000*60)) / (1000))
    const paddedHours = String(hours).padStart(2, '0');
    const paddedMinutes = String(minutes).padStart(2, '0');
    const paddedSeconds = String(seconds).padStart(2, '0');

    timer.textContent = `${paddedHours}:${paddedMinutes}:${paddedSeconds}`;
}
function render_current_session(session_data){
    if (session_data == null){
        active_session_div.innerHTML="";
        no_active_session_div.innerHTML=`
            <p>📚 No Active Session</p>
            <p>Start a new session to begin tracking.</p>
        `;
    }
    else{
        const start_time = new Date(session_data.start_time)
        no_active_session_div.innerHTML="";
        active_session_div.innerHTML=`
            <p><strong>Subject:</strong> <span id="current-subject">${session_data.subject}</span></p>
            <p><strong>Notes:</strong> <span id="current-notes">${session_data.notes}</span></p>
            <p><strong>Started:</strong> <span id="start-time">${start_time}</span></p>
            <!-- timer section  -->
            <p><strong>⏱ Timer:</strong> <span id="timer">00:00:00</span></p>
            <button id="stop-button">Stop Session</button>
        `;
    
        setInterval(()=> show_timer(session_data.start_time), 1000)
        const stop_button = document.getElementById("stop-button");
        stop_button.addEventListener("click", ()=> stop_session(session_data.id))
    }
}
start_button.addEventListener("click", (event) => start_session(event))
get_active_session()