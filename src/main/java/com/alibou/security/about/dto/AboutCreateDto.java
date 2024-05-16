package com.alibou.security.about.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class AboutCreateDto {
    private String description;
    private String descriptionRu;
    private String descriptionEn;
}
