package com.alibou.security.administration;

import com.alibou.security.administration.dto.AdministrationEnDto;
import com.alibou.security.administration.dto.AdministrationResponseDto;
import com.alibou.security.administration.dto.AdministrationRuDto;
import com.alibou.security.administration.dto.AdministrationUzDto;
import com.alibou.security.administration.entity.Administration;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
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
public class AdministrationController {
    private final AdministrationService administrationService;
    @GetMapping("/uz/administration")
    public ResponseEntity<List<AdministrationUzDto>> getAdministrationUz() {
        return ResponseEntity.ok(administrationService.getAdministrationUz());
    }
    @GetMapping("/ru/administration")
    public ResponseEntity<List<AdministrationRuDto>> getAdministrationRu() {
        return ResponseEntity.ok(administrationService.getAdministrationRu());
    }
    @GetMapping("/en/administration")
    public ResponseEntity<List<AdministrationEnDto>> getAdministrationEn() {
        return ResponseEntity.ok(administrationService.getAdministrationEn());
    }
    @GetMapping("/administration/{id}")
    public ResponseEntity<AdministrationResponseDto> getAdministrationEn(@PathVariable UUID id) {
        return ResponseEntity.ok(administrationService.getAdministration(id));
    }

    @GetMapping("/download/{fileId}")
    public ResponseEntity<Resource> downloadImage(@PathVariable String fileId) throws Exception {
        Administration administration = administrationService.getImage(fileId);
        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType(administration.getFileType()))
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + administration.getFileName())
                .body(new ByteArrayResource(administration.getBytes()));
    }
}
