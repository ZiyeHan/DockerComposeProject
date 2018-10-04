$(document).ready(function() {
    let Table = $("#log-table").DataTable({
        data:[],
        columns: [
            { "data": "timestamp"  },
            { "data": "camera" },
            { "data": "event" }
        ],
        rowCallback: function (row, data) {},
        filter: false,
        info: false,
        ordering: false,
        processing: true,
        retrieve: true        
    });

    $("#camera1").click(function(e) {
        $.ajax({
            url: "http://localhost:7999/logs?cam=camera1",
            method: "get",
            success: function(result) {
                console.log(result);
                let originalDictStr = JSON.parse(result);
                let logs = recreateDict(originalDictStr, 'Camera #1');
                Table.clear().draw();
                Table.rows.add(logs).draw();
            },
            error: function(result) {
                alert(JSON.stringify(result))
            }
        });
    });

    $("#camera2").click(function(e) {
        $.ajax({
            url: "http://localhost:7999/logs?cam=camera2",
            method: "get",
            success: function(result) {
                let originalDictStr = JSON.parse(result);
                let logs = recreateDict(originalDictStr, 'Camera #2');
                Table.clear().draw();
                Table.rows.add(logs).draw();
            },
            error: function(result) {
                alert(JSON.stringify(result))
            }
        });
    });

    $("#camera3").click(function(e) {
        $.ajax({
            url: "http://localhost:7999/logs?cam=camera3",
            method: "get",
            success: function(result) {
                let originalDictStr = JSON.parse(result);
                let logs = recreateDict(originalDictStr, 'Camera #3');
                Table.clear().draw();
                Table.rows.add(logs).draw();
            },
            error: function(result) {
                alert(JSON.stringify(result))
            }
        });
    });

    function recreateDict(originalDictStr, cameraId){
        let logDict = [];
        originalDictStr = originalDictStr.split('\'').join('"');
        originalDictStr = originalDictStr.split('": u"').join('": "');
        let originalDict = JSON.parse(originalDictStr)
        for (let timestamp in originalDict){
            logDict.push({
                timestamp: timestamp,
                camera: cameraId,
                event: originalDict[timestamp]
            });
        }
        return logDict;
    }

});

