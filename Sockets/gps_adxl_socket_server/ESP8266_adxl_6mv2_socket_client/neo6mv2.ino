
// Función que retorna un String con todo los datos 
// que recibe el módulo GPS-6MV2 en la comunicación serial
String neo6mv2data() {
  int satellites = 0;
  float hdop = 0.0;
  float location_lat = 0.0;
  float location_lng = 0.0;
  int age = 0;
  char dateBuffer[10]; // 00/00/0000
  char timeBuffer[8]; // 00:00:00
  float altitude = 0.0;
  float course = 0.0;
  float speed = 0.0;

  if (gps.satellites.isValid()) satellites = gps.satellites.value();
  if (gps.hdop.isValid()) hdop = gps.hdop.hdop();
  if (gps.location.isValid()) location_lat = gps.location.lat();
  if (gps.location.isValid()) location_lng = gps.location.lng();
  if (gps.location.isValid()) age = gps.location.age();
  if (gps.altitude.isValid()) altitude = gps.altitude.meters();
  if (gps.course.isValid()) course = gps.course.deg();
  // Serial.println(TinyGPSPlus::cardinal(gps.course.deg()));
  if (gps.speed.isValid()) speed = gps.speed.kmph();

  if (gps.date.isUpdated())
    {
    sprintf(dateBuffer, "%d/%d/%d", gps.date.day(), gps.date.month(), gps.date.year());
    gpsdate = String(dateBuffer);
    }

  if (gps.time.isUpdated())
    {
    sprintf(timeBuffer, "%d:%d:%d", gps.time.hour(), gps.time.minute(), gps.time.second());
    gpstime = String(timeBuffer);
    }

  return "<gps" 
            + String(satellites)
            + " " 
            + String(hdop)
            + " " 
            + String(location_lat,6)
            + " "
            + String(location_lng,6)
            + " "
            + String(age)
            + " "
            + String(gpsdate)
            + " "
            + String(gpstime)
            + " "
            + String(altitude, 2)
            + " "
            + String(course, 2)
            + " "
            + String(speed, 2)
            + ">";
}