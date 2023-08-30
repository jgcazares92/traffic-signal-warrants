"""
Traffic Signal Warrant Tool
Based on MUTCD Chapter 4C

Author: Jerry Cazares
Date: August 2, 2023
"""

'''
Warrant 1: Eight-Hour Vehicle Volume
Condition A, Minimum Vehicle Volume:
   - Intended for locations where large volume
     of intersecting traffic is the principal reason to consider
     installing an traffic signal.
Condition B, Interruption of Continuous Traffic:
   - Intended for application at locations where Condition A
     is not satisfied & where traffic volume on a major street
     is so heavy that traffic on a minor intersecting street
     suffers excessive delay or conflict in entering or
     crossing the major street.

Satisfying conditions:
- Condition A is satisfied
OR
- Condition B is satisfied
OR 
- Combination of 80% of both A and B is satisfied
''' 
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import csv


def read_volume_data(filename):
	df = pd.read_csv(filename)
	return df

def get_hourly_vols(df, major1='NB'):
	N = 4
	if major1 == 'NB':
		major2 = 'SB'
		minor1 = 'EB'
		minor2 = 'WB'
	else:
		major2 = 'WB'
		minor1 = 'NB'
		minor2 = 'SB'
	s = df.groupby(df.index // N).sum()
	time = np.arange(1, 25, 1)
	time = [f"{t}:00" for t in time]
	time_df = pd.DataFrame(time, columns=['Time'])
	s['Time'] = time_df['Time']
	s['SumMajor'] = s[major1] + s[major2]
	s['HighMinor'] = s[[minor1, minor2]].max(axis=1)
	s['SumMajor&HighMinor'] = s['SumMajor'] + s['HighMinor']
	s['Rank'] = s['SumMajor&HighMinor'].rank(ascending=False)
	return s

def get_highest_8hrs(df):
	# Using rank from df, get the highest 8 hours
	h = df.sort_values('Rank')
	df_8hr = h.groupby('Rank').filter(lambda x: x['Rank']<=8)
	# df_4hr = df_8hr.groupby('Rank').filter(lambda x: x['Rank']<=4)

	print(df_8hr)
	return df_8hr#, df_4hr

def w1_cond_a(vals):
	match vals:
		case (1, 1, major, minor, rural):
			if major > 500 and minor > 150 and not rural:
				return True
			elif major > 350 and minor > 105 and rural:
				return True
			else:
				return False
		case (2, 1, major, minor, rural):
			if major > 600 and minor > 150 and not rural:
				return True
			elif major > 420 and minor > 105 and rural:
				return True
			else:
				return False
		case (2, 2, major, minor, rural):
			if major > 600 and minor > 200 and not rural:
				return True
			elif major > 420 and minor > 140 and rural:
				return True
			else:
				return False
		case (1, 2, major, minor, rural):
			if major > 500 and minor > 200 and not rural:
				return True
			elif major > 350 and minor > 140 and rural:
				return True
			else:
				return False
		case _:
			raise TypeError("Condition A cannot be evaluated with provided information. Check inputs.")

def w1_cond_b(vals):
	match vals:
		case (1, 1, major, minor, rural):
			if major > 750 and minor > 75 and not rural:
				return True
			elif major > 525 and minor > 53 and rural:
				return True
			else:
				return False
		case (2, 1, major, minor, rural):
			if major > 900 and minor > 75 and not rural:
				return True
			elif major > 630 and minor > 53 and rural:
				return True
			else:
				return False
		case (2, 2, major, minor, rural):
			if major > 900 and minor > 100 and not rural:
				return True
			elif major > 630 and minor > 70 and rural:
				return True
			else:
				return False
		case (1, 2, major, minor, rural):
			if major > 750 and minor > 100 and not rural:
				return True
			elif major > 525 and minor > 70 and rural:
				return True
			else:
				return False
		case _:
			raise TypeError("Condition B cannot be evaluated with provided information. Check inputs.")

def w1_cond_ab(vals):
	cond_a = False
	cond_b = False
	match vals:
		case (1, 1, major, minor, rural):
			if not rural:
				if major > 400 and minor > 120:
					cond_a = True
				if major > 600 and minor > 60:
					cond_b = True
			else:
				if major > 280 and minor > 84:
					cond_a = True
				if major > 420 and minor > 42:
					cond_b = True
			if cond_a and cond_b:
				return True
			else:
				return False
		case (2, 1, major, minor, rural):
			if not rural:
				if major > 480 and minor > 120:
					cond_a = True
				if major > 720 and minor > 60:
					cond_b = True
			else:
				if major > 336 and minor > 84:
					cond_a = True
				if major > 504 and minor > 42:
					cond_b = True
			if cond_a and cond_b:
				return True
			else:
				return False
		case (2, 2, major, minor, rural):
			if not rural:
				if major > 480 and minor > 160:
					cond_a = True
				if major > 720 and minor > 80:
					cond_b = True
			else:
				if major > 336 and minor > 112:
					cond_a = True
				if major > 504 and minor > 56:
					cond_b = True
			if cond_a and cond_b:
				return True
			else:
				return False
		case (1, 2, major, minor, rural):
			if not rural:
				if major > 400 and minor > 160:
					cond_a = True
				if major > 600 and minor > 80:
					cond_b = True
			else:
				if major > 280 and minor > 112:
					cond_a = True
				if major > 420 and minor > 56:
					cond_b = True
			if cond_a and cond_b:
				return True
			else:
				return False
		case _:
			raise TypeError("Combination Condition cannot be evaluated with provided information. Check inputs.")

def w2_cond(vals):
	hrs_over = 0
	match vals:
		case (1, 1, major, minor, rural):
			if not rural:
				y = [80 if x >= 1092 else 550.22697349-0.6996510769*x+0.0002462697*(x**2) for i, x in enumerate(major)]
				
			else:
				y = [60 if x >= 782 else 377.22710663-0.6793503652*x+0.0003501046*(x**2) for i, x in enumerate(major)]
				
			for i, y_i in enumerate(minor):
				if y_i > y[i]:
						hrs_over+=1
				if hrs_over >= 4:
					return True
				else:
					return False
		case (1, 2, major, minor, rural):
			if not rural:
				x = major
				y = [115 if x >= 1118 else 651.50622395-0.7483745392*x+0.000240228*(x**2) for i, x in enumerate(major)]
				
			else:
				x = major
				y = [80 if x >= 797 else 460.53837044-0.7635806818*x+0.0003591016*(x**2) for i, x in enumerate(major)]
				
			for i, y_i in enumerate(minor):
				if y_i > y[i]:
						hrs_over+=1
				if hrs_over >= 4:
					return True
				else:
					return False
		case (2, 2, major, minor, rural):
			if not rural:
				x = major
				y = [115 if x >= 1295 else 879.232228-1.011380233*x+0.0003253082*(x**2) for i, x in enumerate(major)]
				
			else:
				x = major
				y = [80 if x >= 890 else 613.77772474-0.9893678281*x+0.0004377428*(x**2) for i, x in enumerate(major)]
				
			for i, y_i in enumerate(minor):
				if y_i > y[i]:
						hrs_over+=1
				if hrs_over >= 4:
					return True
				else:
					return False
		case (2, 1, major, minor, rural):
			if not rural:
				x = major
				y = [80 if x >= 1340 else 651.50622395-0.7483745392*x+0.000240228*(x**2) for i, x in enumerate(major)]
				
			else:
				x = major
				y = [60 if x >= 940 else 460.53837044-0.7635806818*x+0.0003591016*(x**2) for i, x in enumerate(major)]
				
			for i, y_i in enumerate(minor):
				if y_i > y[i]:
						hrs_over+=1
				if hrs_over >= 4:
					return True
				else:
					return False
		case _:
			raise TypeError("Warrant 2 cannot be evaluated with provided information. Check inputs.")

def w3_cond(vals):
	hrs_over = 0
	match vals:
		case (1, 1, major, minor, rural):
			if not rural:
				y = [100 if x >= 1516 else 745.652000052-0.7548866636*x+0.00021703*(x**2) for i, x in enumerate(major)]
				
			else:
				y = [75 if x >= 1054 else 520.01155026-0.7647561999*x+0.0003250549*(x**2) for i, x in enumerate(major)]
				
			for i, y_i in enumerate(minor):
				if y_i > y[i]:
						hrs_over+=1
				if hrs_over >= 4:
					return True
				else:
					return False
		case (2, 1, major, minor, rural):
			if not rural:
				x = major
				y = [100 if x >= 1759 else 837.59424427-0.7219511908*x+0.0001720248*(x**2) for i, x in enumerate(major)]
				
			else:
				x = major
				y = [75 if x >= 1196 else 593.38729059-0.7471500045*x+0.000262383*(x**2) for i, x in enumerate(major)]
				
			for i, y_i in enumerate(minor):
				if y_i > y[i]:
						hrs_over+=1
				if hrs_over >= 4:
					return True
				else:
					return False
		case (2, 2, major, minor, rural):
			if not rural:
				x = major
				y = [150 if x >= 1672 else 1060.5405451-0.889969286*x+0.0002059999*(x**2) for i, x in enumerate(major)]
				
			else:
				x = major
				y = [100 if x >= 1183 else 771.842673-0.9817221615*x+0.0003498922*(x**2) for i, x in enumerate(major)]
				
			for i, y_i in enumerate(minor):
				if y_i > y[i]:
						hrs_over+=1
				if hrs_over >= 4:
					return True
				else:
					return False
		case (1, 2, major, minor, rural):
			if not rural:
				x = major
				y = [150 if x >= 1461 else 837.59424427-0.7219511908*x+0.0001720248*(x**2) for i, x in enumerate(major)]
				
			else:
				x = major
				y = [100 if x >= 1040 else 593.38729059-0.7471500045*x+0.000262383*(x**2) for i, x in enumerate(major)]
				
			for i, y_i in enumerate(minor):
				if y_i > y[i]:
						hrs_over+=1
				if hrs_over >= 4:
					return True
				else:
					return False
		case _:
			raise TypeError("Warrant 2 cannot be evaluated with provided information. Check inputs.")


def evaluate_warrant1(volumes, lanes, rural=False, a=False, b=False, c=False):

	major = volumes[0]
	minor = volumes[1]

	print("Volume on both major street approaches {:.1f} vehs/hr".format(major))
	print("Volume on higher-volume minor street approach {:.1f} vehs/hr".format(minor))

	lanes_major = lanes[0]
	lanes_minor = lanes[1]

	evaluation_info = (min(lanes_major,2), min(lanes_minor,2), major, minor, rural)

	a = w1_cond_a(evaluation_info)
	if a:
		print("Warrant 1, Condition A has been satisfied")
	else:
		print("Warrant 1, Condition A could not be satisified. Check Condition B.")

	if not a:
		b = w1_cond_b(evaluation_info)
		if b:
			print("Warrant 1, Condition B has been satisfied")
		else:
			print("Warrant 1, Condition B could not be satisified. Check Combination Conditions.")
	if not a and not b:
		c = w1_cond_ab(evaluation_info)
		if c:
			print("Warrant 1, Conditions A+B Combo been satisfied")
		else:
			print("Warrant 1, Conditions A+B Combo could not be satisified. Cannot satisfy Warrant 1.")
	return [a,b,c]

def evaluate_warrant2(volumes, lanes, rural=False, satisfied=False):
	'''
	Warrant 2: Four-Hour Vehicle Volume
	- Traffic control signal shall be considered if an engineering study finds that,
	  for each of any 4 hours of an average day, the plotted points representing vehs/hr
	  on the major street (total of both approaches) and the corresponding vehs/hr on
	  the higher-volume minor street all fall above the applicable curve
	  in Figure 4C-1 for the existing combination of approach lanes. On the minor street,
	  the higher volume shall not be required to be on the same approach during each
	  of these 4 hours. 
	''' 
	evaluation_info = (min(lanes_major,2), min(lanes_minor,2), volumes[0], volumes[1], rural)
	satisfied = w2_cond(evaluation_info)
	if satisfied:
		print("Warrant 2 has been satisfied.")
	else:
		print("Warrant 2 has not been satisfied.")

	return satisfied

def evaluate_warrant3(volumes, lanes, rural=False, satisfied=False):
	'''
	Warrant 3: Peak Hour
	- This warrant shall be applied only in unusual cases, such as office complexes,
	  manufacturing plants, industrial complexes, or high-occupancy vehicle facilities
	  that attract or discharge large numbers of vehicles over a short time.

	  The need for a traffic control signal shall be considered if an engineering study
	  finds that the criteria in either of the following two categories are met:
	  A. If all three following conditions exist for the same 1 hour (any four consecutive
	  15-minute periods) of an average day:
	    1. The total stopped time delay experienced by the traffic on one minor street
	       approach (one direction only) controleld by a STOP sign equals or exceeds:
	       4 vehicle-hours for a one-lane approach or 5 vehicle-hours for a two lane approach; and
	    2. The volume on the same minor street approach (one direction only) equals or exceeds
	       100 vehs/hr for one moving lane of traffic or 150 veh/hr for two moving lanes; and
	    3. The total entering volume serviced during the hour equals or exceeds 650 vehs/hr
	       for intersections with three approaches or 800 vehs/hr for intersections with
	       four or more approaches.
	  B. The plotted point representing the vehs/hr on the major street (total of both approaches)
	     and the corresponding vehs/hr on the higher-volume minor-street approach (one direction only)
	     for 1 hour (any four consecutive 15-minute periods) of an average day falls above the
	     applicable curve in Figure 4C-3 for the existing combination of approach lanes.
	'''
	evaluation_info = (min(lanes_major,2), min(lanes_minor,2), volumes[0], volumes[1], rural)
	satisfied = w3_cond(evaluation_info)
	if satisfied:
		print("Warrant 3 has been satisfied.")
	else:
		print("Warrant 3 has not been satisfied.")

	return satisfied



if __name__ == '__main__':

	debug = False
	directions = {0: ['NB','SB'], 1: ['EB','WB']}
	major = None
	minor = None
	major_sel = input('Please select the major approach\n0: NB/SB\n1: EB/WB\n')
	if major_sel == '0':
		major = directions[0]
		minor = directions[1]
	else:
		major = directions[1]
		minor = directions[0]

	print("Major approach: ", major)

	vol_df = read_volume_data("sample_intersection_data.csv")
	s = get_hourly_vols(vol_df, major[0])
	df_8hr = get_highest_8hrs(s)


	speed_limit = 40 # mph
	speed_85th = 40 # mph
	population = 10000
	rural = False
	lanes_major = 1
	lanes_minor = 1

	speed_limit = int(input('Speed limit (mph): '))
	speed_85th = int(input('85th % Speed (mph): '))
	speed_warrant = max(speed_limit, speed_85th)
	population = int(input('Area population: '))
	lanes_major = int(input('Number of lanes on major approach: '))
	lanes_minor = int(input('Number of lanes on minor approach: '))

	w1_cond_a_satisfied = False
	w1_cond_b_satisfied = False
	w1_cond_ab_satisfied = False
	w2_satisfied = False
	w3_satisfied = False

	print('\nPREPARING TO EVALUATE WARRANT 1')

	# Rural or urban conditions?
	if speed_warrant > 40 or population < 10000:
		rural = True
		print("Rural conditions satisfied.")
	else:
		print("Rural conditions unsatisfied. Proceed w/ urban conditions.")

	# Need a more universal way of determining major and minor directions...
	if debug:
		vol_8hr_major_nb = [125, 250, 123, 120, 173, 238, 225, 150]
		vol_8hr_major_sb = [125, 225, 122, 120, 172, 450, 225, 150]
		vol_8hr_minor_1d = [100, 149, 125, 75, 80, 90, 75, 70]
	else:
		vol_8hr_major_nb = df_8hr[major[0]].tolist()
		vol_8hr_major_sb = df_8hr[major[1]].tolist()
		vol_8hr_minor_1d = df_8hr['HighMinor'].tolist()
	vol_8hr_major_total = [vol_8hr_major_nb[i]+vol_8hr_major_sb[i] for i in range(len(vol_8hr_major_nb))]
	major = max(vol_8hr_major_total)
	minor = max(vol_8hr_minor_1d)


	w1 = evaluate_warrant1((major, minor), (lanes_major, lanes_minor), rural)
	w1_cond_a_satisfied = w1[0]
	w1_cond_b_satisfied = w1[1]
	w1_cond_ab_satisfied = w1[2]

	w2_satisfied = evaluate_warrant2((vol_8hr_major_total, vol_8hr_minor_1d), (lanes_major, lanes_minor), rural)

	# Check if in approved zone for warrant 3, if not and if satisfied, then recommend flashing
	# during non peak hours
	w3_satisfied = evaluate_warrant3((vol_8hr_major_total, vol_8hr_minor_1d), (lanes_major, lanes_minor), rural)


w2_x1 = np.arange(380, 1410, 10)
w2_y1 = [80 if x >= 1092 else 550.22697349-0.6996510769*x+0.0002462697*(x**2) for i, x in enumerate(w2_x1)]
w2_x2 = np.arange(390, 1410, 10)
w2_y2 = [80 if x >= 1340 else 651.50622395-0.7483745392*x+0.000240228*(x**2) for i, x in enumerate(w2_x2)]
w2_x3 = w2_x2
w2_y3 = [115 if x >= 1118 else 651.50622395-0.7483745392*x+0.000240228*(x**2) for i, x in enumerate(w2_x3)]
w2_x4 = np.arange(450, 1410, 10)
w2_y4 = [115 if x >= 1295 else 879.232228-1.011380233*x+0.0003253082*(x**2) for i, x in enumerate(w2_x4)]


w3_x1 = np.arange(440, 1810, 10)
w3_y1 = [100 if x >= 1516 else 745.652000052-0.7548866636*x+0.00021703*(x**2) for i, x in enumerate(w3_x1)]
w3_x2 = np.arange(515, 1810, 10)
w3_y2 = [100 if x >= 1759 else 837.59424427-0.7219511908*x+0.0001720248*(x**2) for i, x in enumerate(w3_x2)]
w3_x3 = w3_x2
w3_y3 = [150 if x >= 1461 else 837.59424427-0.7219511908*x+0.0001720248*(x**2) for i, x in enumerate(w3_x3)]
w3_x4 = np.arange(590, 1810, 10)
w3_y4 = [150 if x >= 1672 else 1060.5405451-0.889969286*x+0.0002059999*(x**2) for i, x in enumerate(w3_x4)]


fig, ax = plt.subplots(2, 1)
ax[0].plot(w2_x1, w2_y1)
ax[0].plot(w2_x2, w2_y2)
ax[0].plot(w2_x3, w2_y3)
ax[0].plot(w2_x4, w2_y4)
ax[0].plot(vol_8hr_major_total, vol_8hr_minor_1d, 'ko')
ax[0].set_xticks(np.arange(300,1410,100))
ax[0].set_xlim(right=1400, left=300)
ax[0].set_ylim(top=500, bottom=0)
ax[0].title.set_text('Warrant 2: Four-Hour Vehicle Volume')
ax[0].set_ylabel('Minor Street\n-Higher Volume Approach-\nVPH)')
ax[0].set_xlabel("Major Street\n-Total of Both Approaches-\n(VPH)")
ax[0].grid(True)

ax[1].plot(w3_x1, w3_y1)
ax[1].plot(w3_x2, w3_y2)
ax[1].plot(w3_x3, w3_y3)
ax[1].plot(w3_x4, w3_y4)
ax[1].plot(vol_8hr_major_total, vol_8hr_minor_1d, 'ko')
ax[1].set_xticks(np.arange(400,1810,100))
ax[1].set_xlim(right=1800, left=400)
ax[1].set_ylim(top=600, bottom=0)
ax[1].title.set_text('Warrant 3: Peak Hour Volume')
ax[1].set_ylabel('Minor Street\n-Higher Volume Approach-\nVPH)')
ax[1].set_xlabel("Major Street\n-Total of Both Approaches-\n(VPH)")
ax[1].grid(True)
plt.show()