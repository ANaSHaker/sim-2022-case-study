<p align="center"><img src="assets/banner.png" alt="SIM 2022 — Saudi International Maritime Forum" width="100%"></p>
<h1 align="center">SIM 2022</h1>
<p align="center"><b>The official companion app for the Saudi International Maritime Forum 2022 — agenda, speakers, delegations, exhibitors, live stream and networking in one place.</b></p>
<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android%20%7C%20iOS-0F172A?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/Flutter-2.x-02569B?style=flat-square&logo=flutter&logoColor=white" alt="Flutter">
  <img src="https://img.shields.io/badge/State-Bloc%20%2B%20GetX-8B5CF6?style=flat-square" alt="Bloc + GetX">
  <img src="https://img.shields.io/badge/Backend-REST%20%2B%20Firebase-FFCA28?style=flat-square&logo=firebase&logoColor=black" alt="REST + Firebase">
  <img src="https://img.shields.io/badge/Offline-Hive-2F7DD1?style=flat-square" alt="Hive">
  <img src="https://img.shields.io/badge/Event-Nov%202022-38BDF8?style=flat-square" alt="Event app">
  <img src="https://img.shields.io/badge/Case%20Study-portfolio-111827?style=flat-square" alt="Case Study">
</p>

> ℹ️ Case study — the source code is proprietary to the client and is not included.

## Overview

The **Saudi International Maritime Forum (SIM)** is organised by the **Royal Saudi Naval Forces (RSNF)** and brings together naval delegations, maritime companies and industry leaders. For the 2022 edition I built the forum's official mobile app: a pocket guide for attendees, delegations and exhibitors before and during the three event days.

| | |
|---|---|
| **Client** | Event app for the Royal Saudi Naval Forces' maritime forum |
| **Users** | Attendees, official delegations, speakers, sponsors and exhibitors |
| **Platforms** | Android (Google Play) and iOS (App Store, "SIM 2022") — listings retired after the event |
| **My role** | Flutter developer — the full app, from architecture to store release |
| **Timeline** | Built August – October 2022, live for the forum (agenda: 15 – 17 November) |

## The challenge

- **A hard deadline.** An event app is useless one day late — it had to be on both stores before the forum opened.
- **A lot of content, changing until the last minute.** Agenda, speakers, delegations, sponsors, exhibitors, news and media were updated by the organisers right up to the event.
- **Venue connectivity.** Exhibition halls are crowded; content already seen, favourites and notes had to stay available offline.
- **International audience.** Arabic and English, readable in light and dark, with official protocol content (about the forum, the RSNF and the Kingdom).

## Highlights

**🗓️ Programme**
- Three-day agenda with session times, linked speakers, "Ask a question" and a jump to the live stream
- Speakers and delegations with photos, titles and biographies
- Bilateral-meeting section for delegations

**🏢 Exhibition**
- Sponsors and exhibitors with profile, website and contact
- Floor plans, show guide and venue location with in-app directions (Google Maps + route polyline)

**📺 Media**
- Live stream ("SIM Live"), news, photo galleries and video centre (YouTube player)
- About SIM, about the RSNF and about the Kingdom

**👤 Personal**
- Account sign-in and profile, personal **QR badge**
- One-to-one chat between attendees (Firestore)
- Favourites (speakers, delegations, sponsors, exhibitors, news) and personal notes — stored offline
- Search across speakers and sponsors, Arabic / English, light / dark mode, push notifications, help centre and FAQs

## Screens

<p align="center"><img src="assets/screens-1.png" alt="Forum guide screens" width="100%"></p>
<p align="center"><sub>Home hub, about SIM 2022, agenda, sponsor profile and video centre.</sub></p>

<p align="center"><img src="assets/screens-2.png" alt="More screens" width="100%"></p>
<p align="center"><sub>Photo galleries, RSNF page, navigation drawer in light theme, settings and personal notes.</sub></p>

## Signature feature — the whole forum in one pocket hub

<p align="center"><img src="assets/feature-hub.png" alt="Forum hub and agenda" width="100%"></p>

**How it works**
1. The home screen is a single grid of 14 entry points (About SIM, Agenda, Speakers, Delegations, SIM Live, Sponsors, Exhibitors, About KSA, Bilateral Meeting, Floor Plans, Media Center, Show Guide, RSNF, Location), so any content is one tap away.
2. Speakers, delegations, sponsors, exhibitors, banners and photos live in **Cloud Firestore**, so the organisers could update content up to the last minute without a new release — and Firestore's on-device cache keeps already-loaded pages readable when the hall Wi-Fi drops.
3. Anything the attendee stars — speakers, delegations, sponsors, exhibitors, news — is saved in typed Hive boxes, together with personal notes, and shown in a tabbed Favourites screen.
4. From any session the attendee can ask a question or jump straight to the live stream.

## Architecture & stack

```mermaid
flowchart LR
  UI[Screens<br/>home hub · agenda · speakers · sponsors · media · chat]
  subgraph State["State"]
    CU[Cubits<br/>Speakers · About · Media · Social · User · Drawer]
    GX[GetX<br/>routing · translations]
    TP[Provider<br/>theme]
  end
  API[(REST via Dio<br/>media · YouTube Data API)]
  HIVE[(Hive<br/>offline content · favourites · notes)]
  FB[Firebase<br/>Auth · Firestore content & chat · Storage · FCM]
  MAP[Google Maps<br/>directions]
  YT[YouTube / video player]

  UI --> CU & GX & TP
  CU --> API
  CU --> HIVE
  CU --> FB
  UI --> MAP
  UI --> YT
```

| Layer | Tech |
|---|---|
| UI | Flutter, `flutter_screenutil`, `flutter_zoom_drawer`, staggered grid & animations, shimmer, `clay_containers` |
| State | `flutter_bloc` (Cubits per feature) + GetX (`GetMaterialApp`, translations) + Provider (theme) |
| Content | Cloud Firestore (speakers, delegations, sponsors, exhibitors, banners, photos); Dio + YouTube Data API (media, playlists) |
| Offline | Hive with generated type adapters (notes, favourite speakers / sponsors / news) |
| Firebase | Auth, Cloud Firestore (content + chat), Storage, Messaging |
| Maps | `google_maps_flutter`, `geolocator`, `flutter_polyline_points` |
| Media | `youtube_player_flutter`, `video_player`, `webview_flutter`, image download / gallery save |
| Other | `qr_flutter` (personal badge), `flutter_typeahead` (search), `flutter_email_sender` (support), share & rate |

## Engineering notes

- **Content the organisers can change live.** Event data sits in Firestore collections, so late changes to speakers, sponsors or banners reached every phone without a store update; Firestore's local cache covers flaky venue connectivity, and Hive holds everything personal (favourites, notes).
- **Typed favourites.** Favourites use separate Hive boxes with generated adapters per type (speakers, delegations, sponsors, exhibitors, news), which kept the Favourites tabs simple and fast.
- **Directions to the venue.** The location screen draws the route on Google Maps by decoding the directions polyline, from the attendee's current position.
- **Attendee chat.** Messages are stored per user pair in Cloud Firestore (`Users → chats → messages`) and streamed live.
- **Two languages, two themes.** GetX translations for Arabic / English and a persisted dark-mode preference applied at start-up.
- **Built to a fixed date.** Feature-per-folder Cubits let screens be built and shipped in parallel; the app went from first commit to stores in about two months.

## Results

- Delivered and published on **Google Play and the App Store** ("SIM 2022") for the forum in **November 2022**.
- Covered **14 content areas** of the forum in a single app.
- The listings were retired after the event, as is common for single-edition event apps.

## بالعربي

**SIM 2022** هو التطبيق الرسمي للمنتدى البحري السعودي الدولي 2022 الذي نظّمته **القوات البحرية الملكية السعودية**.
يجمع التطبيق كل ما يحتاجه الزائر: جدول المنتدى لثلاثة أيام، المتحدثين والوفود، الرعاة والعارضين، مخططات القاعات، البث المباشر والمركز الإعلامي، والطريق إلى مكان الحدث.
المحتوى يُدار من Firestore ويتحدّث لحظيًا دون إصدار جديد، والمفضلة والملاحظات الشخصية محفوظة على الجهاز (Hive)، ودردشة بين الزوار، وبطاقة QR شخصية.
يدعم العربية والإنجليزية والوضعين الفاتح والداكن، وتم نشره على Google Play وApp Store قبل موعد المنتدى.
دوري: تطوير التطبيق بالكامل بـ Flutter من المعمارية حتى النشر.

## Links

- The store listings (Google Play `com.app.sim.sim`, App Store "SIM 2022") were retired after the event.
- Screenshots in this repository come from the original public showcase of the app.

---
<h3 align="center">Built by Mahmoud Shaker — Senior Flutter Engineer</h3>
<p align="center">
  <a href="https://wa.me/201140279111"><img src="https://img.shields.io/badge/WhatsApp-Chat-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp"></a>
  <a href="https://www.linkedin.com/in/anashaker/"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="https://anashaker.github.io/shaker_portfolio/"><img src="https://img.shields.io/badge/Portfolio-Visit-111827?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Portfolio"></a>
  <a href="mailto:mahmoudshaker382001@gmail.com"><img src="https://img.shields.io/badge/Email-Hire%20me-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
  <a href="https://khamsat.com/user/sheko201566"><img src="https://img.shields.io/badge/Khamsat-Services-F39C12?style=for-the-badge" alt="Khamsat"></a>
  <a href="https://mostaql.com/u/ShekoShaker"><img src="https://img.shields.io/badge/Mostaql-Freelance-2386C8?style=for-the-badge" alt="Mostaql"></a>
  <a href="https://github.com/ANaSHaker"><img src="https://img.shields.io/badge/GitHub-More%20work-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
</p>
