function FileSystem($cordovaFile, $cordovaFileTransfer){
	var download = function(details, success, error, process){
		$cordovaFileTransfer.download(details.url, details.targetPath, details.options, details.trustHosts)
		.then(success, error, process);
	};

	var upload = function(details, success, error, process){
		$cordovaFileTransfer.upload(details.server, details.targetPath, details.options, details.trustHosts)
		.then(success, error, process);
	};

	var fileExists = function(filename, success, error){
		$cordovaFile.checkFile(cordova.file.dataDirectory, filename)
		.then(success, error);
	};

	var getFile = function(srcFile, callbacks){
		$cordovaFile.checkFile(cordova.file.dataDirectory, srcFile)
		.then(function (success) {
			$cordovaFile.readAsText(cordova.file.dataDirectory, srcFile)
			.then(function (result) {
				if(callbacks.success) callbacks.success(result);
			}, function (error) {
				if(callbacks.error) callbacks.error(error);
			});
		}, function (error) {
			if(callbacks.nofile) callbacks.nofile(error);
		});
	};

	return {
		download: download,
		upload: upload,
		fileExists: fileExists,
		getFile: getFile
	};
};
