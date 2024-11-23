Install this script with a simple command line

```sh
mkdir -p $HOME/userScripts && (cd $HOME/userScripts && [ ! -d 42autoLock ] && git clone https://github.com/TuskarMA/42autoLock || (cd 42autoLock && git pull)) && echo -e '\n# Check if the logscreen script is running\nif ! [ -f /tmp/logscreen.lock ]; then\n    python3 $HOME/userScripts/42autoLock/logscreen.py &\nfi' >> $HOME/.profile && source $HOME/.profile && echo -e "Downloaded and runned py script from ddivaev\nModified .profile to run this script every time on log\nScript is now RUNNING"
```
