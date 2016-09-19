# SleeGR

Installationscript for Ubuntu:
------------------------------

```bash
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo apt-get install matplotlib python3 python3-pip
sudo apt-get build-dep python-matplotlib
sudo service mongod start
git clone git@bitbucket.org:skorkmazISS/iot-final.git
cd iot-final
pip3 install -r requirements.txt

```

If you use another OS, you need to install 
mathplotlib, mongoDB, numpy and skipy.
the required Python packages are listed in requirements.txt.

If you have problems with tha installation, you may want use Anacondapython. This is a framework (for Windows an other OS)
that provides various packages especially for datascienc.
