echo "git checkout" $1
git checkout $1
echo "----------------"
echo "git merge" $2
git merge $2
echo "----------------"
echo "git diff" $1 ".." $2
git diff $1..$2
echo "----------------"
echo "git diff" $1 "..." $2
git diff $1...$2
echo "----------------"
echo "git checkout" $2
git checkout $2
echo "----------------"
