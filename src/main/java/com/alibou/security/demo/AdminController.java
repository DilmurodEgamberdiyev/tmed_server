package com.alibou.security.demo;

import com.alibou.security.about.AboutService;
import com.alibou.security.about.dto.AboutCreateDto;
import com.alibou.security.about.entity.About;
import com.alibou.security.administration.AdministrationService;
import com.alibou.security.administration.dto.AdministrationCreateDto;
import com.alibou.security.administration.entity.Administration;
import com.alibou.security.law.LawService;
import com.alibou.security.law.dto.LawCreateDto;
import com.alibou.security.structure.StructureService;
import com.alibou.security.structure.dto.StructureCreateDto;
import io.swagger.v3.oas.annotations.Hidden;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/admin")
@PreAuthorize("hasRole('ADMIN')")
@RequiredArgsConstructor
public class AdminController {
    private final AboutService aboutService;
    private final AdministrationService administrationService;
    private final LawService lawService;
    private final StructureService structureService;

    @PostMapping("/about")
    @PreAuthorize("hasAuthority('admin:create')")
    public ResponseEntity<AboutCreateDto> createAbout(@RequestBody AboutCreateDto aboutCreateDto) {
        return ResponseEntity.status(HttpStatus.CREATED).body(aboutService.createAbout(aboutCreateDto));
    }

    @PutMapping("/about/{id}")
    @PreAuthorize("hasAuthority('admin:update')")
    public ResponseEntity<About> updateAbout(@RequestBody AboutCreateDto aboutCreateDto, @PathVariable UUID id) {
        return ResponseEntity.status(HttpStatus.OK).body(aboutService.updateAbout(aboutCreateDto, id));
    }

    @DeleteMapping("/about/{id}")
    @PreAuthorize("hasAuthority('admin:delete')")
    public ResponseEntity<Boolean> deleteAbout(@PathVariable UUID id) {
        return ResponseEntity.status(HttpStatus.OK).body(aboutService.delete(id));
    }

    @PostMapping("/administration")
    @PreAuthorize("hasAuthority('admin:create')")
    public ResponseEntity<String> createAdministration(@ModelAttribute AdministrationCreateDto administrationCreateDto) throws Exception {
        administrationService.createAdministration(administrationCreateDto);
        return ResponseEntity.status(HttpStatus.CREATED).body("Created");
    }

    @PutMapping("/administration/{id}")
    @PreAuthorize("hasAuthority('admin:update')")
    public ResponseEntity<String> updateAdministration(@ModelAttribute AdministrationCreateDto administrationCreateDto, @PathVariable UUID id) throws IOException {
        administrationService.updateAdministration(administrationCreateDto, id);
        return ResponseEntity.status(HttpStatus.OK).body("Updated");
    }

    @DeleteMapping("/administration/{id}")
    @PreAuthorize("hasAuthority('admin:delete')")
    public ResponseEntity<String> deleteAdministration(@PathVariable UUID id) {
        administrationService.delete(id);
        return ResponseEntity.status(HttpStatus.OK).body("Deleted");
    }

    @PostMapping("/law")
    @PreAuthorize("hasAuthority('admin:create')")
    public ResponseEntity<String> createLaw(@ModelAttribute LawCreateDto lawCreateDto) throws Exception {
        lawService.createLaw(lawCreateDto);
        return ResponseEntity.status(HttpStatus.CREATED).body("Created");
    }

    @PutMapping("/law/{id}")
    @PreAuthorize("hasAuthority('admin:update')")
    public ResponseEntity<String> updateLaw(@ModelAttribute LawCreateDto lawUpdateDto, @PathVariable UUID id) throws IOException {
        lawService.updateLaw(lawUpdateDto, id);
        return ResponseEntity.status(HttpStatus.OK).body("Updated");
    }

    @DeleteMapping("/law/{id}")
    @PreAuthorize("hasAuthority('admin:delete')")
    public ResponseEntity<String> deleteLaw(@PathVariable UUID id) {
        lawService.delete(id);
        return ResponseEntity.status(HttpStatus.OK).body("Deleted");
    }

    @PostMapping("/structure")
    @PreAuthorize("hasAuthority('admin:create')")
    public ResponseEntity<String> createStructure(@ModelAttribute StructureCreateDto structureCreateDto) throws Exception {
        structureService.createStructure(structureCreateDto);
        return ResponseEntity.status(HttpStatus.CREATED).body("Created");
    }

    @DeleteMapping("/structure/{id}")
    @PreAuthorize("hasAuthority('admin:delete')")
    public ResponseEntity<String> deleteStructure(@PathVariable UUID id) {
        structureService.delete(id);
        return ResponseEntity.status(HttpStatus.OK).body("Deleted");
    }
}
