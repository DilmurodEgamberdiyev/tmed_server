package com.alibou.security.law.dto;

import com.alibou.security.law.entities.LawType;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.web.multipart.MultipartFile;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class LawCreateDto {
    private MultipartFile file;
    private String name;
    private String nameRu;
    private String nameEn;
    private LawType lawType;
    private String link;
}
