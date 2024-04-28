package com.example.hackmap

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.ListView
import org.json.JSONArray

class StatActivity : JsonManager() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_stat)

        val device_name = intent.getStringExtra("device_id")
        val device_id = getObjectId(device_name!!)
        val strings = getStatistics("http://127.0.0.1:8000/graph_data?device_id=$device_id&type=0&interval=5%20minutes")
        var objects: List<String> = emptyList()
        var timestamps: List<String> = emptyList()
        for (i in 0 until strings.length()) {
            objects += strings.getJSONObject(i).getString("value")
            timestamps += strings.getJSONObject(i).getString("time")
        }
        var array : List<String> = emptyList()

        val listOfValues = findViewById<ListView>(R.id.tableOfValues)
        val adapter = ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, objects)
        listOfValues.adapter = adapter

        val listOfTimes = findViewById<ListView>(R.id.tableOfTimes)
        val adapterTimes = ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, timestamps)
        listOfTimes.adapter = adapterTimes
    }
}