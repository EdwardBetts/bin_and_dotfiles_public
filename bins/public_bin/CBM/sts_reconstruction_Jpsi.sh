#This shellscript does the STS reconstruction with and without Jpsi for arg1 events with index varying from arg2 to arg3
#But only in case the corresponding STS job doesn't exist anymore and the output files don't exist yet.

# Check if all parameters are present
# If no, exit
if [ $# -ne 3 ]
then
	echo
	echo 'usage :'
	echo 'sts_reconstruction.sh nEvents start_index end_index'
	echo
	exit 0 
fi

# Create joblist.txt and check if connected to an lxi machine
# If no, exit
cd /s/$USER_flast/data_Jpsi
bjobs>joblist.txt
if [ $? -eq 0 ]
then
  echo "already connected to an lxi machine"
  echo "joblist.txt creation successful"
else
  echo "not connected to an lxi machine"
  echo "joblist.txt creation not successful"
  exit 0
fi

#create jobs
cd /s/$USER_flast/data_Jpsi
for (( i = $2 ; i <= $3 ; i++ ))
	do

            jobname=Jpsi_SIM_01_$i
            if [ $(grep -c $jobname joblist.txt) -eq 0 ];
            then
              echo "$jobname does not exist.";
              filename=`filename_generator "noPluto.Urqmd.auau.25gev.centr.sts_reco." $i ".root"`
              if [ ! -f $filename ];
              then
                      echo "$filename does not exist.";
                      echo "index=$i: creating Jpsi_STS_01_$i";
                      bsub -J Jpsi_STS_01_$i root -l -q .x "~/cbmroot/macro/much/sts_reco_Jpsi.C($1,$i,0,1)";
              fi
            fi
            
            jobname=Jpsi_SIM_10_$i
            if [ $(grep -c $jobname joblist.txt) -eq 0 ];
            then
              echo "$jobname does not exist.";
              filename=`filename_generator "Pluto.noUrqmd.auau.25gev.centr.sts_reco." $i ".root"`
              if [ ! -f $filename ];
              then
                      echo "$filename does not exist.";
                      echo "index=$i: creating Jpsi_STS_10_$i";
                      bsub -J Jpsi_STS_10_$i root -l -q .x "~/cbmroot/macro/much/sts_reco_Jpsi.C($1,$i,1,0)";
              fi
            fi
            
            jobname=Jpsi_SIM_11_$i
            if [ $(grep -c $jobname joblist.txt) -eq 0 ];
            then
              echo "$jobname does not exist.";
              filename=`filename_generator "Pluto.Urqmd.auau.25gev.centr.sts_reco." $i ".root"`
              if [ ! -f $filename ];
              then
                      echo "$filename does not exist.";
                      echo "index=$i: creating Jpsi_STS_11_$i";
                      bsub -J Jpsi_STS_11_$i root -l -q .x "~/cbmroot/macro/much/sts_reco_Jpsi.C($1,$i,1,1)";
              fi
            fi
done
