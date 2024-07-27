package org.example.Controller

import jakarta.servlet.http.HttpServletResponse
import org.springframework.core.io.ClassPathResource
import org.springframework.core.io.Resource
import org.springframework.http.HttpHeaders
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import org.springframework.util.Base64Utils
import java.io.ByteArrayOutputStream



@RestController
@RequestMapping("/api")
class ImageController {
    @GetMapping("/getkeypad")
    fun getKeypadImage(response: HttpServletResponse): ResponseEntity<String> {
        try {
            // 리소스 폴더 내의 모든 이미지 파일 리스트
            val resources: List<Resource> = listOf(
                ClassPathResource("static/keypad/_0.png"),
                ClassPathResource("static/keypad/_1.png"),
                ClassPathResource("static/keypad/_2.png"),
                ClassPathResource("static/keypad/_3.png"),
                ClassPathResource("static/keypad/_4.png"),
                ClassPathResource("static/keypad/_5.png"),
                ClassPathResource("static/keypad/_6.png"),
                ClassPathResource("static/keypad/_7.png"),
                ClassPathResource("static/keypad/_8.png"),
                ClassPathResource("static/keypad/_9.png"),
                ClassPathResource("static/keypad/_blank.png"),
            )

            // 이미지 셔플
            val shuffledResources = resources.shuffled()

            // 첫 번째 이미지를 Base64로 인코딩
            val resource = shuffledResources.firstOrNull()
            val imageBase64 = resource?.inputStream?.use { inputStream ->
                val byteArrayOutputStream = ByteArrayOutputStream()
                inputStream.copyTo(byteArrayOutputStream)
                Base64Utils.encodeToString(byteArrayOutputStream.toByteArray())
            } ?: ""

            return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_TYPE, "application/json")
                .body("{\"image\": \"$imageBase64\"}")

        } catch (e: Exception) {
            return ResponseEntity.status(500).body("Error processing image")
        }
    }
}