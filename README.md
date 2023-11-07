# ADS_basics

## Structure
This repo includes 
- Test scripts to run in carla
- basic tutorials named t1, t2, ...,simple lane etc.
- customly built maps for carla and sumo in osm and xodr format.
- Intersection management using plexe.

## Execution

### Carla scripts

 You can run it normally, just open any town and then run the script .



 ### Sumo tutorials

  open sumo and load any of its sumo.cfg file.

 ### maps
  simulate carla, then cd under PythonApi/util in carla (remember to copy the map in the same folder as config.py)
  and run
  ```
  python3 config.py -x <filename>
  ```

### Intersection simulation and Management
 ```
 cd intersection
```
```
python3 main.py
```
 Here, IM is done using plexe and not through any communication.
 



  
