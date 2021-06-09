# Little-Leffen
## Build Instructions
1. Install packages
	* Libmelee: `pip install libmelee` [documentation](https://libmelee.readthedocs.io/en/latest/)
	* Tensorforce: `pip install tensorforce` [documentation](https://tensorforce.readthedocs.io/en/latest/)
2. Download and install dolphin
	* Follow the *Setup Instructions* section for [Libmelee](https://github.com/altf4/libmelee)
	* Save your dolphin build to the *StreamableDolphin* directory
	* Download a SSB Melee 1.02 ISO. I can't tell you where to find it

## Run Instructions
1. Use `dataset_creator.py` to create simulated training data from Slippi recordings
2. Use functions in `main.py` to train and test the agent