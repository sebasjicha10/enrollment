<h1>Enrollment page</h1>
<h2>Description</h2>
This project consists of a simple enrollment page for courses given by my local university (UCR). <a href="#">Watch a video demo here</a>
<h2>Back End</h2>
<ul>
  <li>Python - Flask</li>
  <li>SQLite</li>
</ul>
<h2>Front End</h2>
<ul>
  <li>HTML</li>
  <li>CSS - BootStrap</li>
  <li>JavaScript</li>
</ul>
<h2>How it works</h2>
<h3>Database</h3> 
To get in, the user can log in, if previously registered, or sign up. </br>
The initial registration works with a predefined database where the university has a list of students and their corresponding students' ids, so it validates that the user is, in fact, a student at UCR.</br>
Tables are used to display and update available courses info, show a history of registrations, and update, create and display information about the students.
<h3>Sessions and Routing</h3> 
The webpage uses sessions to confirm the user is registered, and keep him or her logged in.</br>
Once in, through routing with Flask, and with the use of <strong>JSON</strong> and <strong>JINJA</strong>, the following dynamic functionalities are implemented with Python:
<ul>
  <li><strong>Index Page</strong>, or dashboard, displays a list of the already successfully enrolled courses by the user. One can add courses either by clicking on "Add Course" in the dashboard, or "Enrollment" on the navigation bar, which will redirect the user to <u>Enrollment</u>. Course ID, Name, Schedule, and date and time of Enrollment are dynamically displayed.</li>
  <li><strong>Enrollment</strong>, page where the available course options are displayed, with additional useful information course ID, schedule and spaces left. Only courses with at least 1 space left are displayed and the same course can't be enrolled more than once by the same user. Password is required before submitting, and if successful the course is added to the dashboard, letting the user now the operation was successful via flashing a message.</li>
   <li><strong>Schedule</strong>, option in the nav bar where the user can see a visual aid for a dynamically generated weekly schedule with all of the enrolled courses. </li>
  <li><strong>Personal Info</strong>, accesible too from the nav bar, this page displays user information such as Student ID, Mayor, Phone, and Email. The user has the option to update this information or change his or her passsword.</li>
</ul>
