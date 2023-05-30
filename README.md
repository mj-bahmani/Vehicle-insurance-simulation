# Vehicle-insurance-simulation
this is a simulation project for vehicle insurance organization

Event Types:
<ul>
<li>A: Arrival</li>
<li>DP: Departure</li>
<li>DF: filling the case departure</li>
<li>DC: completing the case departure</li>
<li>DE: expert departure</li>
<li>DSC: submitting complaint departure</li>
<li>PA: second car arrival</li>
<li>OIN: moving from outside to inside</li>
<li>ISEND: find out if simulation should end</li>
</ul>


distributions:
<ul>
<li>arrival: depends on weather and time exponential</li>
<li>photography service time: exponential lambda = 6 </li>
<li>waiting time for single car: exponential lambda = 30</li>
<li>filling the case: triangular min = 5 mod = 6 max = 7</li>
<li>expert service time: exponential lambda = 9</li>
<li>and completing the case: triangular min = 6 max = 8 max = 9</li>
<li>complain part service time: exponential lambda = 15 </li>
</ul>

other parameters
<ul>
<li>probability that a car arrives alone: 0.3 </li>
<li>probability that a customer make a complaint: 0.1</li>

</ul>

