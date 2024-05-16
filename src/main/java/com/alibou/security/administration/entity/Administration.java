package com.alibou.security.administration.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Entity
public class Administration {
    @Id
    private UUID id;

    @Lob
    private byte[] bytes;
    private String fileType;
    private String fileName;

    private String phoneNumber;
    private String email;

    @Enumerated(EnumType.STRING)
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
    @Column(columnDefinition = "text", length = 8192)
    private String jobDescription;
    @Column(columnDefinition = "text", length = 8192)
    private String jobDescriptionRu;
    @Column(columnDefinition = "text", length = 8192)
    private String jobDescriptionEn;
    @Column(columnDefinition = "text", length = 8192)
    private String permission;
    @Column(columnDefinition = "text", length = 8192)
    private String permissionRu;
    @Column(columnDefinition = "text", length = 8192)
    private String permissionEn;
}
