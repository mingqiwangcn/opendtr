max_step=$1
for ((step=0 ; step<=${max_step}; step+=1000))
do
    file_name=./models/fetaqa/eval_metrics_${step}.json
    metric=`grep '"precision_at_1"' ${file_name}`
    echo "step=${step} ${metric}"
done
