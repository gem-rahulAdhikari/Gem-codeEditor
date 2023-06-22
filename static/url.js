var Name="";
var Email="";

var myBoolean = false;
var out =  document.getElementById("output");
var keyout1 =  document.getElementById("keyout");
var submitBtn = document.getElementById("myButton");



submitBtn.addEventListener('click', function() {
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
   // const submissionInput=document.getElementById("submission");
    Name=nameInput.value;
    Email=emailInput.value;
   // Submission=submissionInput.value
    console.log('Name:', nameInput.value);
    console.log('Email:', emailInput.value);
    myFunction(nameInput.value, emailInput.value)
   
   // getSubmission(nameInput.value, emailInput.value,submissionInput.value);
    //getSubmission(Name,Email,Submission)
   // setDetails(nameInput.value,emailInput.value,submissionInput.value);
  });


 /* function getSubmission(Name,Email,Submission)
{
   
fetch('https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getSubmission')
.then(response => response.json())
.then(data => {
for (let i = 0; i < data.length; i++) {
 const item = data[i];

 if (item.name === Name && item.email === Email) { // replace 'matched value' with the value you want to match
    anotherBoolean=true;

     console.log(item.submission);
     console.log("Array values:");
   for (let j = 0; j < item.submission.length; j++) {
     console.log(item.submission[j]); // replace 'arrayKey' with the name of the array key
   }
 }
 
}

}

)
.catch(error => console.error(error));

if(myBoolean===false)
{
    setDetails(nameInput.value,emailInput.value,submissionInput.value);
}

}*/


  function myFunction(Name, Email) {
    var Name1=Name;
    var Email1=Email;
   
    // Your function code here
    
    fetch('https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/getSubmission')
.then(response => response.json())
.then(data => {
for (let i = 0; i < data.length; i++) {
 const item = data[i];

 if (item.name === Name && item.email === Email) { // replace 'matched value' with the value you want to match
    myBoolean=true;
    
     console.log(item.url);
     out.value=item.url;
     keyout1.value=item.Key;

   /*for (let j = 0; j < item.submission.length; j++) {
     console.log(item.submission[j]);
     out.innerHTML=item.submission[j];
      // replace 'arrayKey' with the name of the array key
   }*/
   break;
 }
 
}
if(myBoolean===false)
{
    console.log(myBoolean)
    setDetails(Name1,Email1);
}

}

)
.catch(error => console.error(error));


  }

function setDetails(Name,Email){
// Replace with your function name
const apiUrl = `https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/submissions`; // Replace with your app ID and function name
const url2 = 'https://us-east-1.aws.data.mongodb-api.com/app/application-0-awqqz/endpoint/userSubmissions';
const salt = Math.random().toString(36).substring(2, 15);
const stringToHash = Email + salt;
console.log("key " + stringToHash)
var hexHash = CryptoJS.SHA256(stringToHash)
const uniqueUrl = "https://gem-codeeditor.wl.r.appspot.com/?name=".concat(hexHash);
console.log(uniqueUrl)
const salt1 = Math.random().toString(36).substring(2, 15);
const stringToHash1 = salt1;
console.log("key " + stringToHash1)
///document.getElementById("output").innerHTML = uniqueUrl;
const data1 = {
// Replace with your body parameter
"name": Name,
"email": Email,
"url": uniqueUrl,
"Key": stringToHash1,
};

const data2 = {
  "submissions": [],
    "submittedCode": [],
    "inputArray": [],
    "outputArray": [],
    "name":Name,
    "url":uniqueUrl,
    "modified":"",
    "status":"None",
    "key":stringToHash1,
}


out.value=uniqueUrl;
keyout1.value=stringToHash1;

fetch(apiUrl, {
  method: 'POST',
  body: JSON.stringify(data1),
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => {
  // handle the response of the first request
  console.log('Response from API 1:', data);
})
.catch(error => console.error(error));

fetch(url2, {
  method: 'POST',
  body: JSON.stringify(data2),
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => {
  // handle the response of the second request
  console.log('Response from API 2:', data);
})
.catch(error => console.error(error));
}


/*fetch(apiUrl, options)
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error(error));*/









