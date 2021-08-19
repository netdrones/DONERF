#!/bin/bash

SCRIPTNAME="$(basename $0)"
CLEAN=false
OVERLAP_HIGH=0.98

OPTIND=1
while getopts "hci:" opt; do
  	case "$opt" in
	h)
	  	echo "$SCRIPTNAME: flags: -h help, -c clean, -i input_dir, -o overlap_threshold"
		exit 0
		;;
	c)
	  	export CLEAN=true
		;;
	i)
	  	export WORKSPACE_DIR="$OPTARG"
		;;
	o)
	  	export OVERLAP_HIGH="$OPTARG"

	esac
done

shift "$(( OPTIND -1 ))"
if [ -z "$WORKSPACE_DIR" ]; then
  	echo "$SCRIPTNAME: Missing -i argument"
	exit 1
fi

# Ensure that GPU-accelerated OpenCV is installed
if $CLEAN
then
	pip install --upgrade pip
    	if [ ! -d bin/opencv ]; then gsutil -m cp -r gs://netdron.es/opencv bin; fi
    	pip install bin/opencv/*.whl
fi

EXP_NAME=$WORKSPACE_DIR
DOWNSCALE=2
NUM_GPUS="$(nvidia-smi --query_gpu=name --format=csv,noheader | wc -l)"

if [ ! -d "$WORKSPACE_DIR/dense" ]
then
	if [ ! -d $WORKSPACE_DIR/images ]
   	then
		if $CLEAN
		then
		  	mkdir -p $WORKSPACE_DIR/images_cleaned
			python image_utils.py $WORKSPACE_DIR $WORKSPACE_DIR/images_cleaned $OVERLAP_HIGH
			mv $WORKSPACE_DIR/images_cleaned $WORKSPACE_DIR/images
		else
		  	mkdir -p $WORKSPACE_DIR/images
			mv $WORKSPACE_DIR/*.jpg $WORKSPACE_DIR/images 2> /dev/null
			mv $WORKSPACE_DIR/*.jpeg $WORKSPACE_DIR/images 2> /dev/null
			mv $WORKSPACE_DIR/*.png $WORKSPACE_DIR/images 2> /dev/null
			mv $WORKSPACE_DIR/*.JPG $WORKSPACE_DIR/images 2> /dev/null
			mv $WORKSPACE_DIR/*.JPEG $WORKSPACE_DIR/images 2> /dev/null
			mv $WORKSPACE_DIR/*.PNG $WORKSPACE_DIR/images 2> /dev/null

		fi
	else
	  	if $CLEAN
		then
		  	mkdir -p $WORKSPACE_DIR/images_cleaned
		  	python image_utils.py $WORKSPACE_DIR/images $WORKSPACE_DIR/images_cleaned $OVERLAP_HIGH
			rm -r $WORKSPACE_DIR/images
			mv $WORKSPACE_DIR/images_cleaned $WORKSPACE_DIR/images
		else
		  	mkdir -p $WORKSPACE_DIR/images
		  	mv $WORKSPACE_DIR/*.jpg $WORKSPACE_DIR/images 2> /dev/null
			mv $WORKSPACE_DIR/*.jpeg $WORKSPACE_DIR/images 2> /dev/null
			mv $WORKSPACE_DIR/*.png $WORKSPACE_DIR/images 2> /dev/null
			mv $WORKSPACE_DIR/*.JPG $WORKSPACE_DIR/images 2> /dev/null
			mv $WORKSPACE_DIR/*.JPEG $WORKSPACE_DIR/images 2> /dev/null
			mv $WORKSPACE_DIR/*.PNG $WORKSPACE_DIR/images 2> /dev/null

		fi
   	fi
   	sh +x bin/run_colmap.sh $WORKSPACE_DIR
fi

python utils/generate_poses.py $WORKSPACE_DIR
python utils/data_loader.py $WORKSPACE_DIR
python utils/jpt_to_png.py $WORKSPACE_DR/dense/images
rm -f $WORKSPACE_DIR/dense/images/*.jpg
python utils/symlink.py $WORKSPACE_DIR/dense/images $WORKSPACE_DIR
gsutil cp gs://lucas.netdron.es/dataset_info.json $WORKSPACE_DIR
python src/train.py -c configs/DONeRF_2_samples.ini --data $WORKSPACE_DIR --logDir logs
