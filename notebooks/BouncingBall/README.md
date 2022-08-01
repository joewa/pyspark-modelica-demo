## The Bouncing Ball example
This is the model of a bouncing ball:
```modelica
model BouncingBall
  parameter Real e=0.7 "coefficient of restitution";
  parameter Real g=9.81 "gravity acceleration";
  Real h(fixed=true, start=1) "height of ball";
  Real v(fixed=true) "velocity of ball";
  Boolean flying(fixed=true, start=true) "true, if ball is flying";
  Boolean impact;
  Real v_new(fixed=true);
  Integer foo;

equation
  impact = h <= 0.0;
  foo = if impact then 1 else 2;
  der(v) = if flying then -g else 0;
  der(h) = v;

  when {h <= 0.0 and v <= 0.0,impact} then
    v_new = if edge(impact) then -e*pre(v) else 0;
    flying = v_new > 0;
    reinit(v, v_new);
  end when;
end BouncingBall;
```
So the model has two parameters (the coefficient of restitution, e and the gravity accesleration, g) and no timeseries inputs. The challenge could be a parametric simulation with the following input data.
```python
# Running the parametric simulation
ts_sim_df = input_df.groupby(['run_key']).applyInPandas(
        get_sim_func(BouncingBall, 'BouncingBall', res_vars=['h', 'v']), schema=res_schema
    )
