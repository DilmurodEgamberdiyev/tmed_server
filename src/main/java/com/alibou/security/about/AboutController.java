package com.alibou.security.about;

import com.alibou.security.about.dto.AboutEnDto;
import com.alibou.security.about.dto.AboutRuDto;
import com.alibou.security.about.dto.AboutUzDto;
import com.alibou.security.about.entity.About;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/public")
@RequiredArgsConstructor
public class AboutController {
    private final AboutService aboutService;

    @GetMapping("/uz/about")
    public ResponseEntity<List<AboutUzDto>> getAboutUz() {
        return ResponseEntity.ok(aboutService.getAboutUz());
    }

    @GetMapping("/ru/about")
    public ResponseEntity<List<AboutRuDto>> getAboutRu() {
        return ResponseEntity.ok(aboutService.getAboutRu());
    }

    @GetMapping("/en/about")
    public ResponseEntity<List<AboutEnDto>> getAboutEn() {
        return ResponseEntity.ok(aboutService.getAboutEn());
    }

    @GetMapping("/about/{id}")
    public ResponseEntity<About> getAbout(@PathVariable UUID id) {
        return ResponseEntity.ok(aboutService.getAbout(id));
    }
}
