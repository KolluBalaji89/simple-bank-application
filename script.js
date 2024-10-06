let currentUser = null;

function login() {
	const username = document.getElementById("username").value;
	const password = document.getElementById("password").value;
	// Call login API endpoint
	currentUser = { username, password };
	document.getElementById("dashboard").style.display = "block";
}

function logout() {
	currentUser = null;
	document.getElementById("dashboard").style.display = "none";
}

function deposit() {
	document.getElementById("deposit").style.display = "block";
}

function withdraw() {
	document.getElementById("withdraw").style.display = "block";
}

function balanceEnquiry() {
	// Call balance enquiry API endpoint
	const balance = 1000; // Replace with actual balance
	document.getElementById("balance-display").innerText = `Balance: ${balance}`;
}

function depositAmount() {
	const amount = document.getElementById("amount").value;
	// Call deposit API endpoint
	alert(`Deposited ${amount}`);
}

function withdrawAmount() {
	const amount = document.getElementById("amount").value;
	// Call withdraw API endpoint
	alert(`Withdrawn ${amount}`);
}