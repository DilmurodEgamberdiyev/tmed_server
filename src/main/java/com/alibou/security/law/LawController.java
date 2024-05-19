package com.alibou.security.law;

import com.alibou.security.administration.dto.AdministrationResponseDto;
import com.alibou.security.administration.entity.Administration;
import com.alibou.security.law.dto.LawEnDto;
import com.alibou.security.law.dto.LawResponseDto;
import com.alibou.security.law.dto.LawRuDto;
import com.alibou.security.law.dto.LawUzDto;
import com.alibou.security.law.entities.Law;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/public")
public class LawController {
    private final LawService lawService;

    @GetMapping("/uz/law")
    public ResponseEntity<List<LawUzDto>> getLawUz() {
        return ResponseEntity.ok(lawService.getLawUz());
    }

    @GetMapping("/ru/law")
    public ResponseEntity<List<LawRuDto>> getLawRu() {
        return ResponseEntity.ok(lawService.getLawRu());
    }

    @GetMapping("/en/law")
    public ResponseEntity<List<LawEnDto>> getLawEn() {
        return ResponseEntity.ok(lawService.getLawEn());
    }

    @GetMapping("/law/{id}")
    public ResponseEntity<LawResponseDto> getLaw(@PathVariable UUID id) {
        return ResponseEntity.ok(lawService.getLaw(id));
    }

    @GetMapping("/doc/{fileId}")
    public ResponseEntity<Resource> downloadLawDoc(@PathVariable String fileId) throws Exception {
        Law law = lawService.getFile(fileId);
        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType(law.getFileType()))
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + law.getFileName())
                .body(new ByteArrayResource(law.getBytes()));
    }
}
