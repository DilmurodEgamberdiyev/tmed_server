package com.alibou.security.administration;

import com.alibou.security.about.entity.About;
import com.alibou.security.administration.dto.*;
import com.alibou.security.administration.entity.Administration;
import com.alibou.security.exception.ResourceNotFoundException;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.io.IOException;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Transactional
public class AdministrationService {
    private final AdministrationRepository administrationRepository;

    public void createAdministration(AdministrationCreateDto adminCreateDto) throws Exception {
        try {
            String fileName = StringUtils.cleanPath(Objects.requireNonNull(adminCreateDto.getFile().getOriginalFilename()));

            if (fileName.contains("..") || fileName.isBlank()) {
                throw new Exception("Filename contains invalid path sequence " + fileName);
            }

            Administration administration = new Administration(
                    UUID.randomUUID(),
                    adminCreateDto.getFile().getBytes(),
                    adminCreateDto.getFile().getContentType(),
                    fileName,
                    adminCreateDto.getPhoneNumber(),
                    adminCreateDto.getEmail(),
                    adminCreateDto.getAdministrationType(),
                    adminCreateDto.getFullName(),
                    adminCreateDto.getFullNameRu(),
                    adminCreateDto.getFullNameEn(),
                    adminCreateDto.getRole(),
                    adminCreateDto.getRoleRu(),
                    adminCreateDto.getRoleEn(),
                    adminCreateDto.getReceptionDay(),
                    adminCreateDto.getReceptionDayRu(),
                    adminCreateDto.getReceptionDayEn(),
                    adminCreateDto.getJobDescription(),
                    adminCreateDto.getJobDescriptionRu(),
                    adminCreateDto.getJobDescriptionEn(),
                    adminCreateDto.getPermission(),
                    adminCreateDto.getPermissionRu(),
                    adminCreateDto.getPermissionEn()
            );
            administrationRepository.save(administration);
        } catch (Exception e) {
            throw new Exception("Could not save the file " + e);
        }
    }

    public Administration getImage(String fileId) {
        return administrationRepository
                .findById(UUID.fromString(fileId))
                .orElseThrow(() -> new ResourceNotFoundException("Could not find administration with id - " + fileId));
    }

    public List<AdministrationUzDto> getAdministrationUz() {
        List<Administration> administrations = administrationRepository.findAll();

        return administrations.stream().map(admin -> {
            String uriString = uriString(admin.getId().toString());
            return new AdministrationUzDto(
                    admin.getId(),
                    admin.getPhoneNumber(),
                    admin.getEmail(),
                    uriString,
                    admin.getAdministrationType(),
                    admin.getFullName(),
                    admin.getRole(),
                    admin.getReceptionDay(),
                    admin.getJobDescription(),
                    admin.getPermission()
            );
        }).toList();
    }

    public List<AdministrationRuDto> getAdministrationRu() {
        List<Administration> administrations = administrationRepository.findAll();

        return administrations.stream().map(admin -> {
            String uriString = uriString(admin.getId().toString());
            return new AdministrationRuDto(
                    admin.getId(),
                    admin.getPhoneNumber(),
                    admin.getEmail(),
                    uriString,
                    admin.getAdministrationType(),
                    admin.getFullNameRu(),
                    admin.getRoleRu(),
                    admin.getReceptionDayRu(),
                    admin.getJobDescriptionRu(),
                    admin.getPermissionRu()
            );
        }).toList();
    }

    public List<AdministrationEnDto> getAdministrationEn() {
        List<Administration> administrations = administrationRepository.findAll();

        return administrations.stream().map(admin -> {
            String uriString = uriString(admin.getId().toString());
            return new AdministrationEnDto(
                    admin.getId(),
                    admin.getPhoneNumber(),
                    admin.getEmail(),
                    uriString,
                    admin.getAdministrationType(),
                    admin.getFullNameEn(),
                    admin.getRoleEn(),
                    admin.getReceptionDayEn(),
                    admin.getJobDescriptionEn(),
                    admin.getPermissionEn()
            );
        }).toList();
    }

    private String uriString(String id) {
        return ServletUriComponentsBuilder.fromCurrentContextPath()
                .path("/api/v1/public/download/")
                .path(id)
                .toUriString();
    }

    public void updateAdministration(AdministrationCreateDto administrationCreateDto, UUID id) throws IOException {
        Administration administration = administrationRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Could not find administration - " + id));

        administration.setBytes(administrationCreateDto.getFile().getBytes());
        administration.setFileType(administrationCreateDto.getFile().getContentType());
        administration.setFileName(administrationCreateDto.getFile().getOriginalFilename());
        administration.setAdministrationType(administrationCreateDto.getAdministrationType());

        administration.setEmail(administrationCreateDto.getEmail());
        administration.setPhoneNumber(administrationCreateDto.getPhoneNumber());

        administration.setFullName(administrationCreateDto.getFullName());
        administration.setFullNameRu(administrationCreateDto.getFullNameRu());
        administration.setFullNameEn(administrationCreateDto.getFullNameEn());

        administration.setJobDescription(administrationCreateDto.getJobDescription());
        administration.setJobDescriptionRu(administrationCreateDto.getJobDescriptionRu());
        administration.setJobDescriptionEn(administrationCreateDto.getJobDescriptionEn());

        administration.setPermission(administrationCreateDto.getPermission());
        administration.setPermissionRu(administrationCreateDto.getPermissionRu());
        administration.setPermissionEn(administrationCreateDto.getPermissionEn());

        administration.setReceptionDay(administrationCreateDto.getReceptionDay());
        administration.setReceptionDayRu(administrationCreateDto.getReceptionDayRu());
        administration.setReceptionDayEn(administrationCreateDto.getReceptionDayEn());

        administration.setRole(administrationCreateDto.getRole());
        administration.setRoleRu(administrationCreateDto.getRoleRu());
        administration.setRoleEn(administrationCreateDto.getRoleEn());

        administrationRepository.save(administration);
    }

    public void delete(UUID id) {
        administrationRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Could not find administration - " + id));
        administrationRepository.deleteById(id);
    }

    public AdministrationResponseDto getAdministration(UUID id) {
        Administration administration = administrationRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Could not find administration - " + id));
        return new AdministrationResponseDto(
                administration.getId(),
                uriString(administration.getId().toString()),
                administration.getPhoneNumber(),
                administration.getEmail(),
                administration.getAdministrationType(),
                administration.getFullName(),
                administration.getFullNameRu(),
                administration.getFullNameEn(),
                administration.getRole(),
                administration.getRoleRu(),
                administration.getRoleEn(),
                administration.getReceptionDay(),
                administration.getReceptionDayRu(),
                administration.getReceptionDayEn(),
                administration.getJobDescription(),
                administration.getJobDescriptionRu(),
                administration.getJobDescriptionEn(),
                administration.getPermission(),
                administration.getPermissionRu(),
                administration.getPermissionEn()
        );
    }
}
