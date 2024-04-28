package com.example.hackmap

import android.content.Context
import androidx.appcompat.app.AppCompatActivity
import org.json.JSONArray
import org.json.JSONObject
import java.io.BufferedReader
import java.io.FileInputStream
import java.io.FileOutputStream
import java.io.InputStreamReader
import java.io.ObjectInputStream
import java.io.ObjectOutputStream
import java.net.HttpURLConnection
import java.net.URL
import javax.net.ssl.HttpsURLConnection

open class JsonManager: AppCompatActivity() {
    val buildingsJsonArrayName: String = "objects"

    fun readJSON(): String {
        val fin: FileInputStream = openFileInput("objects.json")
        val im = ObjectInputStream(fin)
        val string: String = im.readObject() as String
        im.close()
        fin.close()
        return string


    }

    fun getJson(): JSONArray {
        val jsonData = readJSON()

        val taskJsonString = JSONObject(jsonData)
        val strings = taskJsonString.getJSONArray(buildingsJsonArrayName) as JSONArray

        return strings
    }
    fun getObjects(): List<String> {
        //val strings = getJsonFromServer("http://127.0.0.1:8000/all")
        val strings = getJson()
        var objects: List<String> = emptyList()
        for (i in 0 until strings.length()) {
            objects += strings.getJSONObject(i).getString("name")
        }
        return objects
    }

    fun getObjectLatitudeByName(name: String): Double {

        val strings = getJsonFromServer("http://127.0.0.1:8000/all")

        for (i in 0 until strings.length()) {
            if (strings.getJSONObject(i).getString("name") == name)
                return strings.getJSONObject(i).getDouble("latitude")
        }

        return 0.0
    }
    fun getObjectLongitudeByName(name: String): Double {

        val strings = getJsonFromServer("http://127.0.0.1:8000/all")

        for (i in 0 until strings.length()) {
            if (strings.getJSONObject(i).getString("name") == name)
                return strings.getJSONObject(i).getDouble("longitude")
        }

        return 0.0
    }
    fun getJsonFromServer(address: String): JSONArray {
        val url = URL(address)
        val httpURLConnection = url.openConnection() as HttpsURLConnection
        val inputStream = httpURLConnection.inputStream
        val bufferedReader = BufferedReader(InputStreamReader(inputStream))
        var data = ""
        var line = ""
        lateinit var jsonArray: JSONArray
        while (line != null) {
            data += line
            line = bufferedReader.readLine()
        }
        if (!data.isEmpty()) {
            val jsonObject = JSONObject(data)
            jsonArray = jsonObject.getJSONArray(buildingsJsonArrayName) as JSONArray
        }
        return jsonArray
    }
    fun getObjectLastValue(name: String): Double {
        val strings = getJsonFromServer("https://127.0.0.1:8000/all")

        for (i in 0 until strings.length()) {
            if (strings.getJSONObject(i).getString("name") == name)
                return strings.getJSONObject(i).getDouble("last_value")
        }

        return 0.0
    }

    fun getObjectId(name: String): Int {
        val strings = getJsonFromServer("https://127.0.0.1:8000/all")

        for (i in 0 until strings.length()) {
            if (strings.getJSONObject(i).getString("name") == name)
                return strings.getJSONObject(i).getInt("device_id")
        }

        return 1
    }

    fun getStatistics(address: String = "https://127.0.0.1:8000/graph_data?device_id=1&type=0&interval=5%20minutes"): JSONArray {
        val url = URL(address)
        val httpURLConnection = url.openConnection() as HttpURLConnection
        val inputStream = httpURLConnection.inputStream
        val bufferedReader = BufferedReader(InputStreamReader(inputStream))
        var data = ""
        var line = ""
        lateinit var jsonArray: JSONArray
        while (line != null) {
            data += line
            line = bufferedReader.readLine()
        }
        if (!data.isEmpty()) {
            val jsonObject = JSONObject(data)
            jsonArray = jsonObject.getJSONArray("timestamps") as JSONArray
        }
        return jsonArray
    }
}