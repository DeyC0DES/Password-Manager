package com.password_manager.password_manager.services;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.*;
import java.util.Enumeration;
import java.util.Map;

@Service
public class IpService {

    public String getPublicIp() {
        try {
            URL url = new URL("https://api64.ipify.org?format=text");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String publicIp = reader.readLine();
            reader.close();

            return publicIp;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public String getLocalIp() {
        try {
            Enumeration<NetworkInterface> interfaces = NetworkInterface.getNetworkInterfaces();
            while (interfaces.hasMoreElements()) {
                NetworkInterface networkInterface = interfaces.nextElement();
                Enumeration<InetAddress> address = networkInterface.getInetAddresses();
                while (address.hasMoreElements()) {
                    InetAddress inetAddress = address.nextElement();

                    if (!inetAddress.isLoopbackAddress() && inetAddress instanceof Inet4Address) {
                        return inetAddress.getHostAddress();
                    }
                }
            }
        } catch (SocketException e) {
            e.printStackTrace();
        }
        return "unknown Local IP";
    }

    public String getUserCountry(String ipAddress) {
        String apiURL = "http://ip-api.com/json/" + ipAddress;

        RestTemplate restTemplate = new RestTemplate();
        Map response = restTemplate.getForObject(apiURL, Map.class);

        if ("fail".equals(response.get("status"))) {
            return "Could not determine location: " + response.get("message");
        }

        return response.get("country").toString();
    }

    public String getUserState(String ipAddress) {
        String apiURL = "http://ip-api.com/json/" + ipAddress;

        RestTemplate restTemplate = new RestTemplate();
        Map response = restTemplate.getForObject(apiURL, Map.class);

        if ("fail".equals(response.get("status"))) {
            return "Could not determine location: " + response.get("message");
        }

        return response.get("regionName").toString();
    }

    public String getUserCity(String ipAddress) {
        String apiURL = "http://ip-api.com/json/" + ipAddress;

        RestTemplate restTemplate = new RestTemplate();
        Map response = restTemplate.getForObject(apiURL, Map.class);

        if ("fail".equals(response.get("status"))) {
            return "Could not determine location: " + response.get("message");
        }

        return response.get("city").toString();
    }


}
