#!/bin/bash

# Sadece myapp-deployment ile başlayan podları listelelim olacaktır(Deployment podları).Daha sonra bu podları geçici değişkene aktaracaktır.Bu değişkeni kullanmış olacağız.
PODS=($(kubectl get pods -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | grep '^myapp-deployment'))

# Pod sayısını döndürür ve COUNT değişkenine aktarır.
COUNT=${#PODS[@]}

# POD sayısı sıfır olarak dönerse aşağıdaki mesajı döndürecektir.
if [ $COUNT -eq 0 ]; then
  echo "myapp-deployment ile başlayan pod bulunamadı!"
  exit 1
fi

# Rastgele pod seç ve değişkene aktaracaktır
RANDOM_INDEX=$((RANDOM % COUNT))
SELECTED_POD=${PODS[$RANDOM_INDEX]}

# Silinecek pod'u ekrana yazdıracaktır.
echo "Silinen pod: $SELECTED_POD"

# Podu silecektir.Pod silinmesini beklemeden çıkacaktır.
kubectl delete pod $SELECTED_POD >/dev/null 2>&1 &
