function generate_report() {
    (cd ~/Downloads && python ~/repo/s3-expenses/app.py $1 $2)
}