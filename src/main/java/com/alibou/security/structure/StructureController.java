package com.alibou.security.structure;

import com.alibou.security.structure.dto.StructureResponseDto;
import com.alibou.security.structure.entity.Structure;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/public")
public class StructureController {
    private final StructureService structureService;


    @GetMapping("/structure")
    public ResponseEntity<List<StructureResponseDto>> getStructures() {
        return ResponseEntity.ok(structureService.getStructures());
    }

    @GetMapping("/structure/{fileId}")
    public ResponseEntity<Resource> downloadLawDoc(@PathVariable String fileId) throws Exception {
        Structure structure = structureService.getStructureImage(fileId);
        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType(structure.getFileType()))
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + structure.getFileName())
                .body(new ByteArrayResource(structure.getBytes()));
    }
}
