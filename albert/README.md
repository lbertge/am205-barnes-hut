Generating data:
```py
python numerical_sim_only.py kepler_orbit.txt --alg naive --out kepler_orbit_naive --dt 0.5
python numerical_sim_only.py kepler_orbit.txt --alg leapfrog --out kepler_orbit_leapfrog --dt 0.5
python analytical_sim_only.py --out kepler_orbit_analytical --dt 0.5
```
Generating Animations:
```py
python anim_only.py -n kepler_orbit_analytical kepler_orbit_no_label kepler_orbit_naive --out kepler_orbit --r 10
```
