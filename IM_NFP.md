# Hybrid Model: Zone Infiltration and People Count

Han Li, Tianzhen Hong, Xuan Luo

Lawrence Berkeley National Laboratory

December 6, 2018 


Justification for Feature Update
================================

The proposed new feature improves the current HybridModel modeling
capability (Lee & Hong, 2017) by adding inverse modeling algorithms
based on the zone moisture and contaminant balance equations. The
current HybridModel feature uses measured zone air temperature to
inversely solve the zone internal thermal mass or air infiltration rate
assuming the HVAC system is off and zone is in free-floating mode. The
new HybridModel feature allows additional parameters such as the
measured zone air humidity ratio and CO<sub>2</sub> concentration as the input
to the inverse modeling algorithms to solve the highly uncertain
parameters such as air infiltration and people count. Depending on the
availability of the measured zone supply air parameters (i.e., supply
air flow rate, supply air temperature, supply air humidity ratio, and
supply air CO<sub>2</sub> concentration), the new HybridModel feature can solve
air infiltration and people count for both HVAC-off mode and HVAC-on
mode. The hybrid approach keeps the virtue of the physics-based model
and takes advantage of more measured buildings data which become
available nowadays due to the wide adoption of low-cost sensors and the
needs of better controls in existing buildings. This new feature
proposal provides technical details of the enhanced HybridModel object
and its implementation in EnergyPlus. The proposed feature will improve
simulation usability and accuracy for existing buildings, which supports
more accurate analysis of energy retrofits.

Overview
========

Air Infiltration
----------------

EnergyPlus uses the object, ZoneInfiltration:DesignFlowRate, to
represent the infiltration caused by the opening and closing of exterior
doors, cracks around windows, and even in very small amount through
building elements. Users define the infiltration design air flow rate,
an infiltration schedule, and temperature and wind correction
coefficients. The source code module, ZoneEquipmentManager, contains the
simplified infiltration algorithm as shown in Equation (1).

Infiltration = (Idesign)(Fschedule)[A+B(T_{zone}-T_{odb})+C(WindSpeed)+D(WindSpeed)<sup>2</sup>

Where: <br />
&nbsp;&nbsp;&nbsp;&nbsp;A is the Constant term coefficient <br />
&nbsp;&nbsp;&nbsp;&nbsp;B is the Temperature term coefficient <br />
&nbsp;&nbsp;&nbsp;&nbsp;C is the Velocity term coefficient <br />
&nbsp;&nbsp;&nbsp;&nbsp;D is the Velocity squared coefficient <br />

The simple method has an empirical correlation that modifies the
infiltration as a function of wind speed and temperature difference
across the envelope. The difficulty in using this equation is
determining valid coefficients for each building type in each location.
The simplified infiltration models consider the wind speed on zone
altitude, and the variation in infiltration heat loss based on the wind
velocity. These coefficients vary and provide very different results
that cause great uncertainty in determining which values to use.
EnergyPlus allows users to input these coefficients, however it is not
easy to identify correct ones for typical modeling practices. The
infiltration hybrid model derives the time-step zone infiltration air
flow rates, using the inverse zone heat balance equation, moisture
balance equation, or contaminant balance equation, which consider all
complexities of design flow rate, coefficients and climate conditions.

People Count
------------

In EnergyPlus, people count and people activity level is represented by
the People and corresponding Schedule objects. Users set the number of
people calculation method, people activity level, sensible and fraction
heat fractions, and CO<sub>2</sub> generation rate in the People object. Each
People object can be assigned to a zone or a zone list. A set of people
related schedule objects are used to define the temporal variation of
people count . In typical simulation setting, the People object is
usually set to have fixed schedules. In reality, occupancy schedule is
highly uncertain. Using the typical schedules for the People object can
lead to inaccurate results. The new hybrid model algorithm calculates
the time-step zone people count by inversely solving the zone sensible
heat balance equation, moisture balance equation, or contaminant balance
equation.

Zone Balance Equations
----------------------

The hybrid model algorithms are built upon the physics-based zone heat,
moisture, and contaminant balance equations reformulated to solve a
partially inverse problem. The basis for the zone air system integration
is to formulate balance equations for the zone air and solve the
resulting ordinary differential equations. It should be noted that the
hybrid algorithms to be developed are generic and can be adopted by
EnergyPlus and other building energy simulation programs. Equation (2)
below indicates zone heat balance relationships. It assumes that the sum
of zone loads and air system output equals the change in energy stored
in the zone. The infiltration airflow rate, m$_{inf}$, changes for
different conditions depending on outdoor temperature, wind speed, and
HVAC system operations. The energy provided from systems to the zone is
represented as Q$_{sys}$. $$\begin{aligned}
\rho_{air}V_z C_{p}\frac {dT_z} {dt} &= \Sigma{Q_{in}}+\Sigma{h_i A_i (T_{si}-T_z)} + \Sigma{m_{zi}C_p(T_{zi}-T_z)} \\
+ & m_{inf}C_p(T_o - T_z) + m_{sys}C_p(T_{sys} - T_z) \end{aligned}$$
$$\begin{aligned}
\text{Where: }\\
  \rho_{air} &: \text{Zone air density} ~ [kg/m^{3}], \\
  V_{z} &: \text{Zone air volume} ~ [m^{3}],\\
  C_{p} &: \text{zone air specific heat} ~ [kJ/kg \cdot K],\\
  T_{z} &: \text{zone air temperature at the current time step} ~[K],\\
  T_{si} &: \text{zone surface temperature at the current time step} ~[K],\\
  T_{zi} &: \text{air temperature of a neighboring zone at the current time step} ~[K],\\
  T_{o} &: \text{outdoor air temperature at the current time step} ~[K],\\
  T_{sys} &: \text{HVAC system supply air temperature at the current time step} ~[K],\\
  t &: \text{Current timestamp},\\
  \Sigma{Q_{in}} &: \text{Sum of internal sensible heat gain} ~ ,\\
  \Sigma{h_i A_i (T_{si}-T_z)} &: \text{Convective heat transfer from the zone surfaces} ~ [kW],\\
  \Sigma{m_{zi}C_p(T_{zi}-T_z)} &: \text{Heat transfer due to interzone air mixing} ~ [kW],\\
  m_{inf} (T_o - T_z)&: \text{Heat transfer due to infiltration of outside air} ~ [kW],\\
  m_{sys} (T_{sys} - T_z)&: \text{Heat transfer due to air supplied by HVAC system} ~ [kW],\\\end{aligned}$$

The sum of zone loads and the provided air system energy equals the
change in energy stored in the zone. Typically, the capacitance
$\rho_{air}V_z C_{p}$ would be that of the zone air only. The internal
thermal masses, assumed to be in equilibrium with the zone air, are
included in this term. EnergyPlus provides algorithms to solve the zone
air energy and moisture balance equations defined in the
ZoneAirHeatBalanceAlgorithm object. The algorithms use the finite
difference approximation or analytical solution to calculate the
derivative term with respect to time.

EnergyPlus provides three different heat balance solution algorithms to
solve the zone air energy balance equations. These are defined in the
Algorithm field in the ZoneAirHeatBalanceAlgorithm object:
3rdOrderBackwardDifference, EulerMethod and AnalyticalSolution. The
first two methods to solve Equation use the finite difference
approximation while the third uses an analytical solution. The hybrid
modeling approach uses the 3rdOrderBackwardDifference to inversely solve
the air infiltration. EnergyPlus Code for these balance algorithms are
referenced to the ZoneTempPredictorCorrector module.

Similarly, EnergyPlus solves zone humidity ratio and CO<sub>2</sub>
concentration with the predictor-corrector approach. Equations (3) is
the zone air moisture balance equation.

$$\begin{aligned}
\rho_{air} V_{z} C_{w}\frac {dW_z} {dt} &= \Sigma{kg_{mass_{sched}}} + \Sigma{A_i h_i \rho_{air} (W_{si} - W_z)} + \Sigma{m_{zi} C_p (W_{zi}-W_z)} \\
+ & m_{inf} (W_o - W_z) + m_{sys} (W_{sys} - W_z)\end{aligned}$$

$$\begin{aligned}
\text{Where: }\\
  \rho_{air} &: \text{Zone air density} ~ [kg/m^{3}], \\
  V_{z} &: \text{Zone air volume} ~ [m^{3}],\\
  C_{w} &: \text{Zone air humidity capacity multiplier},\\
  W_{z} &: \text{Zone air humidity ratio} ~ [kg_w/kg_{dry\cdot air}],\\
  W_{si} &: \text{humidity ratio at a zone interior surface at the current time step} ~[kg_w/kg_{dry\cdot air}],\\
  W_{zi} &: \text{air temperature of a neighboring zone at the current time step} ~[kg_w/kg_{dry\cdot air}],\\
  W_{o} &: \text{outdoor air humidity ratio at the current time step} ~[kg_w/kg_{dry\cdot air}],\\
  W_{sys} &: \text{HVAC system supply air humidity ratio at the current time step} ~[kg_w/kg_{dry\cdot air}],\\
  t &: \text{Current timestamp},\\
  \Sigma{kg_{mass_{sched}}} &: \text{sum of scheduled internal moisture load} ~ [kg/s],\\
  \Sigma{A_i h_i \rho_{air} (W_{si} - W_z)} &: \text{Convective moisture transfer from the zone surfaces} ~ [kg/s],\\
  \Sigma{m_{zi} C_p (W_{zi}-W_z)} &: \text{Moisture transfer due to interzone air mixing} ~ [kg/s],\\
  m_{inf} (W_o - W_z)&: \text{Moisture transfer due to infiltration of outside air} ~ [kg/s],\\
  m_{sys} (W_{sys} - W_z)&: \text{Moisture transfer due to air supplied by HVAC system} ~ [kg/s],\\\end{aligned}$$

Equations (4) is the zone air CO<sub>2</sub> balance equation. $$\begin{aligned}
\rho_{air} V_{z} C_{CO_{2}}\frac {dC_z} {dt} &= \Sigma{kg_{mass_{sched}}}\times 10^{6} + \Sigma{m_{zi}(C_{zi}-C_z)} \\
+ & m_{inf} (C_o - C_z) + m_{sys} (C_{sys} - C_z) \end{aligned}$$

$$\begin{aligned}
\text{Where: }\\
  \rho_{air} &: \text{Zone air density} ~ [kg/m^{3}], \\
  V_{z} &: \text{Zone air volume} ~ [m^{3}],\\
  C_{CO_{2}} &: \text{Zone carbon dioxide capacity multiplier [dimensionless]},\\
  C_{z} &: \text{zone air carbon dioxide concentration at the current time step} ~ [ppm],\\
  C_{zi} &: \text{Carbon dioxide concentration in the zone air being transferred into this zone} ~ [ppm],\\
  C_o&: \text{Carbon dioxide concentration in outdoor air} ~ [ppm],\\
  C_{sys}&: \text{Carbon dioxide concentration in the system supply airstream}~ [ppm],\\
  t &: \text{Current time},\\
  \Sigma{kg_{mass_{sched}}} &: \text{Sum of scheduled internal carbon dioxide loads} ~ [kg/s],\\
  \Sigma{m_{zi}(C_{zi}-C_z)} &: \text{Carbon dioxide transfer due to interzone air mixing} ~ [kg/s],\\
  m_{inf} (C_o - C_z)&: \text{Carbon dioxide transfer due to infiltration and ventilation of outdoor air} ~ [kg/
s],\\
  m_{sys} (C_{sys} - C_z)&: \text{Carbon dioxide transfer due to system supply} ~ [kg/s]\\\end{aligned}$$

Technical Approach
==================

This section provides technical details of solving zone balance
equations via third-order backward approximation. Depending on the
available number of zone air parameters (i.e., temperature, humidity
ratio, and CO<sub>2</sub> concentration), there are different inverse solution
scenarios. The figure below shows the different inverse solution
scenarios. Theoritically, more than one un-known parameters (i.e., zone
thermal mass, air infiltration, and people count) could be solved at the
same time if the measurements of zone air temperature, humidity ratio,
and CO<sub>2</sub> concentration are all available. In this new feature, we only
propose the new algorithms to solve one unknown parameter at a time. The
solution scenario details are described in the following sub-sections.

link to the chart

Infiltration Inverse Models
---------------------------

This sub-section shows three scenarios to solve zone air infiltration
with different zone balance equations. Note that the system supply terms
may or may not be included depending on the HVAC system operation
status. The system supply terms should be included if the HybridModel is
used to solve air infiltration when the HVAC system is on. No system
supply term should be included if the HybridModel is used to solve air
infiltration when the HVAC system is off.

### Solving Infiltration with Temperature

$Equation~(2)$ can be re-written with the third-order backward
approximation: $$\begin{aligned}
C_z\frac {\frac{11}{6}T_{z}^{t}-3T_{z}^{t-\delta t}+\frac{3}{2}T_{z}^{t-2\delta t}-\frac{1}{3}T_{z}^{t-3\delta t}} {\delta t} = RHS\end{aligned}$$
Where: $$\begin{aligned}
  RHS = \Sigma{Q_{in}}+\Sigma{h_i A_i (T_{si}-T_z)} + \Sigma{m_{zi}C_p(T_{zi}-T_z)} + m_{inf}C_p(T_o - T_z) + m_{sys}C_p(T_{sys} - T_z)\end{aligned}$$
Then the infiltration mass flow rate can be solved: $$\begin{aligned}
  m_{inf} = \frac{C_z\frac {\frac{11}{6}T_{z}^{t}-3T_{z}^{t-\delta t}+\frac{3}{2}T_{z}^{t-2\delta t}-\frac{1}{3}T_{z}^{t-3\delta t}} {\delta t}-[\Sigma{Q_{in}}+\Sigma{h_i A_i (T_{si}-T_z)} + \Sigma{m_{zi}C_p(T_{zi}-T_z)} + m_{sys}C_p(T_{sys} - T_z)]}{C_p(T_o - T_{z}^{t})}\end{aligned}$$

### Solving Infiltration with Humidity Ratio

$Equation~(3)$ can be re-written with the third-order backward
approximation: $$\begin{aligned}
C_{wz}\frac {\frac{11}{6}W_{z}^{t}-3W_{z}^{t-\delta t}+\frac{3}{2}W_{z}^{t-2\delta t}-\frac{1}{3}W_{z}^{t-3\delta t}} {\delta t} = RHS\end{aligned}$$
Where: $$\begin{aligned}
  RHS &= \Sigma{kg_{mass_{sched}}} + \Sigma{A_i h_i \rho_{air} (W_{si} - W_{z}^{t})} + \Sigma{m_{zi} C_p (W_{zi}-W_{z}^{t})} \\
  &+ m_{inf} (W_o - W_{z}^{t}) + m_{sys} (W_{sys} - W_{z}^{t})\end{aligned}$$
Then the infiltration mass flow rate can be solved: $$\begin{aligned}
  m_{inf} = \frac{C_{wz}\frac {\frac{11}{6}W_{z}^{t}-3W_{z}^{t-\delta t}+\frac{3}{2}W_{z}^{t-2\delta t}-\frac{1}{3}W_{z}^{t-3\delta t}} {\delta t}-[\Sigma{kg_{mass_{sched}}} + \Sigma{A_i h_i \rho_{air} (W_{si} - W_{z}^{t})} + \Sigma{m_{zi} C_p (W_{zi}-W_{z}^{t})}]}{W_o - W_{z}^{t}}\end{aligned}$$

### Solving Infiltration with CO<sub>2</sub> Concentration

$Equation~(4)$ can be re-written with the third-order backward
approximation: $$\begin{aligned}
C_{CO_{2}z}\frac {\frac{11}{6}C_{z}^{t}-3C_{z}^{t-\delta t}+\frac{3}{2}C_{z}^{t-2\delta t}-\frac{1}{3}C_{z}^{t-3\delta t}} {\delta t} = RHS\end{aligned}$$
Where: $$\begin{aligned}
  RHS = \Sigma{kg_{mass_{sched}}}\times 10^{6} + \Sigma{m_{zi}(C_{zi}-C_z)} m_{inf} (C_o - C_z) + m_{sys} (C_{sys} - C_z)\end{aligned}$$
Then the infiltration mass flow rate can be solved: $$\begin{aligned}
  m_{inf} = \frac{C_{CO_{2}z}\frac {\frac{11}{6}C_{z}^{t}-3C_{z}^{t-\delta t}+\frac{3}{2}C_{z}^{t-2\delta t}-\frac{1}{3}C_{z}^{t-3\delta t}} {\delta t}-[\Sigma{kg_{mass_{sched}}}\times 10^{6} + \Sigma{m_{zi}(C_{zi}-C_z)} + m_{sys} (C_{sys} - C_z)]}{C_o - C_{z}^{t}}\end{aligned}$$

People Count Inverse Models
---------------------------

This sub-section shows three scenarios to solve zone people count with
different zone balance equations. Note that the system supply terms may
or may not be included depending on the HVAC system operation status.
The system supply terms should be included if the HybridModel is used to
solve air infiltration when the HVAC system is on. No system supply term
should be included if the HybridModel is used to solve air infiltration
when the HVAC system is off.

### Solving People Count with Temperature

$Equation~(2)$ can be re-written with the third-order backward
approximation: $$\begin{aligned}
C_z\frac {\frac{11}{6}T_{z}^{t}-3T_{z}^{t-\delta t}+\frac{3}{2}T_{z}^{t-2\delta t}-\frac{1}{3}T_{z}^{t-3\delta t}} {\delta t} = RHS\end{aligned}$$
Where: $$\begin{aligned}
  RHS = \Sigma{Q_{in}}+\Sigma{h_i A_i (T_{si}-T_z)} + \Sigma{m_{zi}C_p(T_{zi}-T_z)} + m_{inf}C_p(T_o - T_z) + m_{sys}C_p(T_{sys} - T_z)\end{aligned}$$
The sum of internal sensible heat gains is: $$\begin{aligned}
  \Sigma{Q_{in}} &= C_z\frac {\frac{11}{6}T_{z}^{t}-3T_{z}^{t-\delta t}+\frac{3}{2}T_{z}^{t-2\delta t}-\frac{1}{3}T_{z}^{t-3\delta t}} {\delta t} \\
  &-  [\Sigma{h_i A_i (T_{si}-T_z)} + \Sigma{m_{zi}C_p(T_{zi}-T_z)} + m_{inf}C_p(T_o - T_z) + m_{sys}C_p(T_{sys} - T_z)] \end{aligned}$$
The sum of internal sensible heat gains from people is:
$$\begin{aligned}
  \Sigma{Q_{people}} = \Sigma{Q_{in}} - \Sigma{Q_{others}}\end{aligned}$$
Finally, the number of people could be solved: $$\begin{aligned}
  N = \frac {\Sigma{Q_{people}}}{Q_{single}} \end{aligned}$$

$$\begin{aligned}
\text{Where: }\\
  Q_{single} &: \text{Sensible heat rate per person} ~ [W] \\\end{aligned}$$

### Solving People Count with Humidity Ratio

$Equation~(3)$ can be re-written with the third-order backward
approximation: $$\begin{aligned}
C_{wz}\frac {\frac{11}{6}W_{z}^{t}-3W_{z}^{t-\delta t}+\frac{3}{2}W_{z}^{t-2\delta t}-\frac{1}{3}W_{z}^{t-3\delta t}} {\delta t} = RHS\end{aligned}$$
Where: $$\begin{aligned}
  RHS &= \Sigma{kg_{mass_{sched}}} + \Sigma{A_i h_i \rho_{air} (W_{si} - W_{z}^{t})} + \Sigma{m_{zi} C_p (W_{zi}-W_{z}^{t})} \\
  &+ m_{inf} (W_o - W_{z}^{t}) + m_{sys} (W_{sys} - W_{z}^{t})\end{aligned}$$
The sum of internal moisture gains is: $$\begin{aligned}
  \Sigma{kg_{mass_{sched}}} &= C_{wz}\frac {\frac{11}{6}W_{z}^{t}-3W_{z}^{t-\delta t}+\frac{3}{2}W_{z}^{t-2\delta t}-\frac{1}{3}W_{z}^{t-3\delta t}} {\delta t} \\
  &-  [\Sigma{A_i h_i \rho_{air} (W_{si} - W_{z}^{t})} + \Sigma{m_{zi} C_p (W_{zi}-W_{z}^{t})}] \end{aligned}$$
The sum of internal moisture gains from people is: $$\begin{aligned}
  \Sigma{kg_{mass_{sched-people}}} = \Sigma{kg_{mass_{sched}}} - \Sigma{kg_{mass_{sched-others}}} \end{aligned}$$
Finally, the number of people could be solved: $$\begin{aligned}
  N = \frac {\Sigma{kg_{mass_{sched-people}}}}{kg_{mass_{single}}} \end{aligned}$$
$$\begin{aligned}
\text{Where: }\\
  kg_{mass_{single}} &: \text{Moisture dissipation rate per person} ~ [kg / s] \\\end{aligned}$$

### Solving People Count with CO<sub>2</sub> Concentration

$Equation~(4)$ can be re-written with the third-order backward
approximation: $$\begin{aligned}
C_{CO_{2}z}\frac {\frac{11}{6}C_{z}^{t}-3C_{z}^{t-\delta t}+\frac{3}{2}C_{z}^{t-2\delta t}-\frac{1}{3}C_{z}^{t-3\delta t}} {\delta t} = RHS\end{aligned}$$
Where: $$\begin{aligned}
  RHS = \Sigma{kg_{mass_{sched}}}\times 10^{6} + \Sigma{m_{zi}(C_{zi}-C_z)} m_{inf} (C_o - C_z) + m_{sys} (C_{sys} - C_z)\end{aligned}$$
The sum of internal CO<sub>2</sub> gains is: $$\begin{aligned}
  \Sigma{kg_{mass_{sched}}}\times 10^{6} &= C_{CO_{2}z}\frac {\frac{11}{6}C_{z}^{t}-3C_{z}^{t-\delta t}+\frac{3}{2}C_{z}^{t-2\delta t}-\frac{1}{3}C_{z}^{t-3\delta t}} {\delta t} \\
  &-  [\Sigma{m_{zi}(C_{zi}-C_z)} m_{inf} (C_o - C_z) + m_{sys} (C_{sys} - C_z)] \end{aligned}$$
The sum of internal CO<sub>2</sub> gains from people is: $$\begin{aligned}
  \Sigma{kg_{mass_{sched-people}}} = \Sigma{kg_{mass_{sched}}} - \Sigma{kg_{mass_{sched-others}}} \end{aligned}$$
Finally, the number of people could be solved: $$\begin{aligned}
  N = \frac {\Sigma{kg_{mass_{sched-people}}}}{kg_{mass_{single}}} \end{aligned}$$
$$\begin{aligned}
\text{Where: }\\
  kg_{mass_{single}} &: \text{CO<sub>2</sub> generation rate per person} ~ [m^{3}/(s \cdot W)] \\\end{aligned}$$

Convergence
-----------

There can be many factors affecting the convergence when trying to solve
the differential equation numerically with the third-order backward
approximation. The most common issue is the overflow. For instance, the
indoor-outdoor air temperature difference term $(T_o - T_z)$ can be a
very small number when the two temperatures are very close. Overflow
will happen if the program tries to calculate the air infiltration rate
by dividing the denominator of Equation (6) by $C_p(T_o - T_z)$.
Therefore, conditions checks are needed when implementing the algorithm
in the code. In this case, a threshold of 0.05°C or greater temperature
difference must be met to calculate the infiltration rate at one
timestamp. Similarly, thresholds are added for the algorithms using
humidity ratio and CO<sub>2</sub> concentration. In addition, EnergyPlus uses a
zone predictor-corrector mechanism to calculate the heating or cooling
needs of a zone on HVAC system, and update the zone air parameters based
on the calculated amount of heating or cooling the HVAC system provides
to a zone. The uncertainties such as truncation errors in those
predictor-corrector routines can cause unrealistic in the inverse
modeling routine. Therefore, thresholds for infiltration and people
count calculation are applied to the code. For infiltration, a valid
value must be within the range of 0 to 10 air change per hour. For
people count, the lower bound is zero, and the upper-bound is the total
possible internal heat/moisture/CO<sub>2</sub> gain divided by the
heat/moisture/CO<sub>2</sub> generation rate.

IDD Modifications
=================

New Object(s)
-------------

None

Revised Object(s)
-----------------

We propose to revise the current HybridModel:Zone. The revised object
defines inputs for the new hybrid modeling algorithms for individual
zones.

    HybridModel:Zone,
           \memo Zones with measured data of indoor air temperature, humidity ratio, and 
           CO2 concentration, and a range of dates.
           \memo If the range of temperature measurement dates includes a leap day, the 
           weather data should include a leap day.
    A1 ,   \field Name
           \required-field
           \type alpha
    A2 ,   \field Zone Name
           \required-field
           \type object-list
           \object-list ZoneNames
    A3 ,   \field Calculate Zone Internal Thermal Mass
           \note Use measured temperature to calculate zone temperature capacity multiplier.
           \type choice
           \key No
           \key Yes
           \default No
    A4 ,   \field Calculate Zone Air Infiltration Rate
           \note Use measured zone air parameters (temperature, humidity ratio, or 
           CO2 concentration) to calculate zone air infiltration rate.
           \note At least one measured parameter should be provided.
           \type choice
           \key No
           \key Yes
           \default No
    A5 ,   \field Calculate Zone People Count
           \note Use measured air parameters (temperature, humidity ratio,
    or CO2 concentration) to calculate zone people count.
           \note At least one measured parameter should be provided..
           \type choice
           \key No
           \key Yes
           \default No
    A6 ,   \field Zone Measured Air Temperature Schedule Name
           \type object-list
           \object-list ScheduleNames
           \note Schedule name of the measured zone air temperature.
    A7 ,   \field Zone Measured Air Humidity Ratio Schedule Name
           \type object-list
           \object-list ScheduleNames
           \note Schedule name of the measured zone air humidity ratio.
    A8 ,   \field Zone Measured Air CO2 Concentration Schedule Name
           \type object-list
           \object-list ScheduleNames
           \note Schedule name of the measured zone air CO2 concentration.
    A9 ,   \field Zone Input People Activity Schedule Name
           \type object-list
           \object-list ScheduleNames
           \note Schedule name of the zone people activity level
    A10 ,  \field Zone Input People Sensible Heat Fraction Schedule Name
           \type object-list
           \object-list ScheduleNames
           \note Schedule name of the people's sensible heat fraction.
    A11 ,  \field Zone Input People Radiant Heat Fraction Schedule Name
           \type object-list
           \object-list ScheduleNames
           \note Schedule name of the people's radiant heat fraction.
    A12 ,  \field Zone Input People CO2 Generation Rate Schedule Name
           \type object-list
           \object-list ScheduleNames
           \note Schedule name of the people's CO2 generation rate.
    A13 ,  \field Zone Input Supply Air Temperature Schedule Name
           \type object-list
           \object-list ScheduleNames
           \note Schedule name of the system supply air temperature of the zone.
    A14 ,  \field Zone Input Supply Air Mass Flow Rate Schedule Name
           \type object-list
           \object-list ScheduleNames
           \note Schedule name of the system supply air mass flow rate of the zone.
    A15 ,  \field Zone Input Supply Air Humidity Ratio Schedule Name
           \type object-list
           \object-list ScheduleNames
           \note Schedule name of the system supply air humidity ratio of the zone.
    A16 ,  \field Zone Input Supply Air CO2 Concentration Schedule Name
           \type object-list
           \object-list ScheduleNames
           \note Schedule name of the system supply air CO2 concentration of the zone.
    N1 ,   \field Begin Month
           \required-field
           \minimum 1
           \maximum 12
           \type integer
    N2 ,   \field Begin Day of Month
           \required-field
           \minimum 1
           \maximum 31
           \type integer
    N3 ,   \field End Month
           \required-field
           \minimum 1
           \maximum 12
           \type integer
    N4 ;   \field End Day of Month
           \required-field
           \minimum 1
           \maximum 31
           \type integer

Simulation Process
==================

The hybrid modeling feature uses a new flag, “Hybrid Modeling Flag” in
the sizing and primary simulation in the simulation manager. “Hybrid
Modeling Flag” is triggered by inputs in the new object,
“HybridModel:Zone”. The flag triggers the hybrid model simulation that
calculates the zone temperature capacitance multipliers, infiltration
air flow rates, or people count depending on the user’s input in the
object, and the zone air temperature data input in the Schedule:File
objects. The simulation steps will be as follows depending on the inputs
of the HybridModel:Zone object.

Solve Zone Air Infiltration
---------------------------

When the “Calculate Zone Air Infiltration Rate” flag is set to YES and
the “Calculate Zone People Count” flag is set to NO:

1.  One of the following schedules must be provided to trigger the
    inverse solution: (1) Zone Measured Air Temperature Schedule
    Name, (2) Zone Measured Air Humidity Ratio Schedule Name, (3) Zone
    Measured Air CO2 Concentration Schedule Name.

2.  One of the following schedule pairs can be supplemented to the
    corresponding zone measured air parameters above to trigger the
    inverse solution with system supply terms included: (1) Zone Supply
    Air Temperature Schedule Name, and Zone Supply Air Mass Flow Rate
    Schedule Name, (2) Zone Supply Air Humidity Ratio Schedule Name, and
    Zone Supply Air Mass Flow Rate Schedule Name, (3) Zone Supply Air
    CO2 Concentration Schedule Name, and Zone Supply Air Mass Flow Rate
    Schedule Name.

3.  If Zone Measured Air Temperature Schedule, Zone Supply Air
    Temperature Schedule, and Zone Supply Air Mass Flow Rate Schedule
    are all provided, the hybrid model simulation will solve the zone
    air infiltration with the system supply terms included in the zone
    sensible heat balance equation. Otherwise, the hybrid simulation
    will treat the system as free-floating if Zone Supply Air
    Temperature Schedule, and Zone Supply Air Mass Flow Rate Schedule
    are not provided.

4.  If Zone Measured Air Humidity Ratio Schedule, Zone Supply Air
    Humidity Ratio Schedule, and Zone Supply Air Mass Flow Rate Schedule
    are all provided, the hybrid model simulation will solve the zone
    air infiltration with the system supply terms included in the zone
    moisture balance equation. Otherwise, the hybrid simulation will
    treat the system as free-floating if Zone Supply Air Humidity Ratio
    Schedule, and Zone Supply Air Mass Flow Rate Schedule are not
    provided.

5.  If Zone Measured Air CO<sub>2</sub> concentration Schedule, Zone Supply Air
    CO<sub>2</sub> Schedule, and Zone Supply Air Mass Flow Rate Schedule are all
    provided, the hybrid model simulation will solve the zone air
    infiltration with the system supply terms included in the zone
    CO<sub>2</sub> balance equation. Otherwise, the hybrid simulation will treat
    the system as free-floating if Zone Supply Air CO<sub>2</sub> Schedule, and
    Zone Supply Air Mass Flow Rate Schedule are not provided.

When the above conditions are met, the hybrid model simulation will
solve the zone air infiltration and conduct normal energy simulation
with the calculated infiltration.

Solve Zone People Count
-----------------------

When the “Calculate Zone Air Infiltration Rate” flag is set to NO and
the “Calculate Zone People Count” flag is set to YES:

1.  One of the following schedules must be provided to trigger the
    inverse solution: (1) Zone Measured Air Temperature Schedule
    Name, (2) Zone Measured Air Humidity Ratio Schedule Name, (3) Zone
    Measured Air CO2 Concentration Schedule Name.

2.  One of the following schedule pairs can be supplemented to the
    corresponding zone measured air parameters above to trigger the
    inverse solution with system supply terms included: (1) Zone Supply
    Air Temperature Schedule Name, and Zone Supply Air Mass Flow Rate
    Schedule Name, (2) Zone Supply Air Humidity Ratio Schedule Name, and
    Zone Supply Air Mass Flow Rate Schedule Name, (3) Zone Supply Air
    CO2 Concentration Schedule Name, and Zone Supply Air Mass Flow Rate
    Schedule Name.

3.  The Zone Input People Activity Schedule Name can be provided to
    specify people’s activity level at different times. If it is not
    provided, a default value of 130 W/person will be used in the hybrid
    simulation. The Zone Input People Sensible Heat Fraction Schedule
    Name can be provided to specify people’s sensible heat fraction at
    different times. If it is not provided, a default value of 0.6 will
    be used in the hybrid simulation. The Zone Input People Radiant Heat
    Fraction Schedule Name can be provided to specify people’s radiant
    heat portion of the sensible at different times. If it is not
    provided, a default value of 0.3 will be used in the hybrid
    simulation.

4.  If Zone Measured Air Temperature Schedule, Zone Supply Air
    Temperature Schedule, and Zone Supply Air Mass Flow Rate Schedule
    are all provided, the hybrid model simulation will solve the zone
    people count with the system supply terms included in the zone
    sensible heat balance equation. Otherwise, the hybrid simulation
    will treat the system as free-floating if Zone Supply Air
    Temperature Schedule, and Zone Supply Air Mass Flow Rate Schedule
    are not provided.

5.  If Zone Measured Air Humidity Ratio Schedule, Zone Supply Air
    Humidity Ratio Schedule, and Zone Supply Air Mass Flow Rate Schedule
    are all provided, the hybrid model simulation will solve the zone
    people count with the system supply terms included in the zone
    moisture balance equation. Otherwise, the hybrid simulation will
    treat the system as free-floating if Zone Supply Air Humidity Ratio
    Schedule, and Zone Supply Air Mass Flow Rate Schedule are not
    provided.

6.  If Zone Measured Air CO<sub>2</sub> concentration Schedule, Zone Supply Air
    CO<sub>2</sub> Schedule, and Zone Supply Air Mass Flow Rate Schedule are all
    provided, the hybrid model simulation will solve the zone people
    count with the system supply terms included in the zone CO<sub>2</sub>
    balance equation. Otherwise, the hybrid simulation will treat the
    system as free-floating if Zone Supply Air CO<sub>2</sub> Schedule, and Zone
    Supply Air Mass Flow Rate Schedule are not provided.

When the above conditions are met, the hybrid model simulation will
solve the zone people count and conduct normal energy simulation.

IO Ref
======

Two new output variables are defined:

    1. Variable: Infiltration Air Change per Hour.
    Units: N/A
    Variable reference: Zone(Loop). InfilOAAirChangeRateHM Index type key: Zone
    Variable type key: Average
    Keyed value: Zone(Loop).Name

    2. Variable: Zone Hybrid Model People Count
    Units: N/A
    Variable reference: Zone(Loop).NumOccHM Index type key: Zone
    Variable type key: Average
    Keyed value: Zone(Loop).Name

Testing/Validation/Data Source(s)
=================================

A two-story building model in Chicago climate will be used. The model
will first be run in normal simulation model to produce hourly schedules
of zone air temperature, humidity, CO<sub>2</sub> concentration, and people
count in the zone. Then the office model will be modified to run in the
inverse mode taking the simulated results of zone air temperature,
humidity, CO<sub>2</sub> concentration as input to compute the zone air
infiltration rate and people count, which can be verified against the
original input (ground truth) of the zone air infiltration rate and
people count.

EngRef
======

TBD

Example File
============

An revised example file based on modifications to the current example
HybrideModel building model will be developed to demonstrate the new
feature.

Reference
=========

Lee, S. H., & Hong, T. (2017). Leveraging Zone Air Temperature Data to
Improve Physics-Based Energy Simulation of Existing Buildings Lawrence
Berkeley National Laboratory , Berkeley , United States, 1223–1230.
