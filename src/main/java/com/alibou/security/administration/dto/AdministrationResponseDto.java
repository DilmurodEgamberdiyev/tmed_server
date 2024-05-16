package com.alibou.security.administration.dto;

import com.alibou.security.administration.entity.AdministrationType;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class AdministrationResponseDto {
    private UUID id;
    private String image;
    private String phoneNumber;
    private String email;
    private AdministrationType administrationType;
    private String fullName;
    private String fullNameRu;
    private String fullNameEn;
    private String role;
    private String roleRu;
    private String roleEn;
    private String receptionDay;
    private String receptionDayRu;
    private String receptionDayEn;
    private String jobDescription;
    private String jobDescriptionRu;
    private String jobDescriptionEn;
    private String permission;
    private String permissionRu;
    private String permissionEn;

}
