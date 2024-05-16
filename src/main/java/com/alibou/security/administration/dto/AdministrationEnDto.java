package com.alibou.security.administration.dto;

import com.alibou.security.administration.entity.AdministrationType;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;
@Data
@AllArgsConstructor
@NoArgsConstructor
public class AdministrationEnDto {
    private UUID id;
    private String phoneNumber;
    private String email;
    private String image;
    private AdministrationType administrationType;
    private String fullName;
    private String role;
    private String receptionDay;
    private String jobDescription;
    private String permission;
}
